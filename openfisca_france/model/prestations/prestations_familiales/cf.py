# -*- coding: utf-8 -*-


# OpenFisca -- A versatile microsimulation software
# By: OpenFisca Team <contact@openfisca.fr>
#
# Copyright (C) 2011, 2012, 2013, 2014, 2015 OpenFisca Team
# https://github.com/openfisca
#
# This file is part of OpenFisca.
#
# OpenFisca is free software; you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# OpenFisca is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from __future__ import division

from numpy import (round, maximum as max_, minimum as min_, logical_not as not_, logical_or as or_)

from ...base import *  # noqa analysis:ignore


@reference_formula
class cf_enfant_a_charge(SimpleFormulaColumn):
    column = BoolCol(default = False)
    entity_class = Individus
    label = u"Complément familial - Enfant considéré à charge"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        est_enfant_dans_famille = simulation.calculate('est_enfant_dans_famille', period)
        smic55 = simulation.calculate('smic55', period)
        age = simulation.calculate('age', period)
        rempli_obligation_scolaire = simulation.calculate('rempli_obligation_scolaire', period)

        pfam = simulation.legislation_at(period.start).fam

        condition_enfant = ((age >= pfam.cf.age1) * (age < pfam.enfants.age_intermediaire) *
            rempli_obligation_scolaire)
        condition_jeune = (age >= pfam.enfants.age_intermediaire) * (age < pfam.cf.age2) * not_(smic55)

        return period, or_(condition_enfant, condition_jeune) * est_enfant_dans_famille


@reference_formula
class cf_ressources_i(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Individus
    label = u"Complément familial - Ressources de l'individu prises en compte"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        br_pf_i = simulation.calculate('br_pf_i', period)
        est_enfant_dans_famille = simulation.calculate('est_enfant_dans_famille', period)
        cf_enfant_a_charge = simulation.calculate('cf_enfant_a_charge', period)

        return period, or_(not_(est_enfant_dans_famille), cf_enfant_a_charge) * br_pf_i


@reference_formula
class cf_plafond(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Plafond d'éligibilité au Complément Familial"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        pfam = simulation.legislation_at(period.start).fam

        isol = simulation.calculate('isol', period)
        biact = simulation.calculate('biact', period)
        cf_enfant_a_charge_holder = simulation.compute('cf_enfant_a_charge', period)

        # Calcul du nombre d'enfants à charge au sens du CF
        cf_nbenf = self.sum_by_entity(cf_enfant_a_charge_holder)

        # Calcul du taux à appliquer au plafond de base
        taux_plafond = 1 + pfam.cf.majoration_plafond_tx1 * min_(cf_nbenf, 2) + pfam.cf.majoration_plafond_tx2 * max_(cf_nbenf - 2, 0)

        # Majoration du plafond pour biactivité ou isolement
        majoration_plafond = (isol | biact)

        plafond = pfam.cf.plafond * taux_plafond + pfam.cf.majoration_plafond_biact_isole * majoration_plafond

        return period, plafond


@reference_formula
class cf_majore_plafond(DatedFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Plafond d'éligibilité au Complément Familial majoré"

    @dated_function(date(2014, 4, 1))
    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        plafond_base = simulation.calculate('cf_plafond', period)
        pfam = simulation.legislation_at(period.start).fam
        return period, plafond_base * pfam.cf.plafond_cf_majore


@reference_formula
class cf_ressources(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Ressources prises en compte pour l'éligibilité au complément familial"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        cf_ressources_i_holder = simulation.compute('cf_ressources_i', period)
        ressources = self.sum_by_entity(cf_ressources_i_holder)
        return period, ressources


@reference_formula
class cf_eligibilite_base(SimpleFormulaColumn):
    column = BoolCol
    entity_class = Familles
    label = u"Éligibilité au complément familial sous condition de ressources et avant cumul"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')
        cf_enfant_a_charge_holder = simulation.compute('cf_enfant_a_charge', period)
        cf_nbenf = self.sum_by_entity(cf_enfant_a_charge_holder)
        return period, cf_nbenf >= 3


@reference_formula
class cf_non_majore_avant_cumul(SimpleFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Complément familial non majoré avant cumul"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        eligibilite_base = simulation.calculate('cf_eligibilite_base', period)
        ressources = simulation.calculate('cf_ressources', period)
        plafond = simulation.calculate('cf_plafond', period)

        pfam = simulation.legislation_at(period.start).fam

        # Complément familial
        eligibilite = eligibilite_base * (ressources <= plafond)
        montant = pfam.af.bmaf * pfam.cf.tx

        # Complément familial différentiel
        plafond_diff = plafond + 12 * montant
        eligibilite_diff = not_(eligibilite) * eligibilite_base * (
            ressources <= plafond_diff)
        montant_diff = (plafond_diff - ressources) / 12

        return period, max_(eligibilite * montant, eligibilite_diff * montant_diff)


@reference_formula
class cf_majore_avant_cumul(DatedFormulaColumn):
    column = FloatCol
    entity_class = Familles
    label = u"Complément familial majoré avant cumul"

    @dated_function(date(2014, 4, 1))
    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        eligibilite_base = simulation.calculate('cf_eligibilite_base', period)
        ressources = simulation.calculate('cf_ressources', period)
        plafond_majore = simulation.calculate('cf_majore_plafond', period)

        pfam = simulation.legislation_at(period.start).fam

        eligibilite = eligibilite_base * (ressources <= plafond_majore)
        montant = pfam.af.bmaf * pfam.cf.tx_majore

        return period, eligibilite * montant


@reference_formula
class cf_temp(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Complément familial avant d'éventuels cumuls"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('month')

        cf_non_majore_avant_cumul = simulation.calculate('cf_non_majore_avant_cumul', period)
        cf_majore_avant_cumul = simulation.calculate('cf_majore_avant_cumul', period)

        return period, max_(cf_non_majore_avant_cumul, cf_majore_avant_cumul)


@reference_formula
class cf(SimpleFormulaColumn):
    column = FloatCol(default = 0)
    entity_class = Familles
    label = u"Complément familial"
    url = "http://vosdroits.service-public.fr/particuliers/F13214.xhtml"

    def function(self, simulation, period):
        '''
        L'allocation de base de la paje n'est pas cumulable avec le complément familial
        '''
        period = period.start.offset('first-of', 'month').period('month')
        paje_base_temp = simulation.calculate('paje_base_temp', period)
        apje_temp = simulation.calculate_divide('apje_temp', period)
        ape_temp = simulation.calculate_divide('ape_temp', period)
        cf_temp = simulation.calculate('cf_temp', period)
        residence_mayotte = simulation.calculate('residence_mayotte', period)

        cf_brut = (paje_base_temp < cf_temp) * (apje_temp <= cf_temp) * (ape_temp <= cf_temp) * cf_temp
        return period, not_(residence_mayotte) * round(cf_brut, 2)
