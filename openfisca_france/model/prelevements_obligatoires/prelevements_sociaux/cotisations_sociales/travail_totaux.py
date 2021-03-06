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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


from __future__ import division


import logging


from ....base import *  # noqa analysis:ignore


log = logging.getLogger(__name__)


@reference_formula
class cotisations_employeur(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales patronales"
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        period = period
        cotisations_employeur_contributives = simulation.calculate('cotisations_employeur_contributives', period)
        cotisations_employeur_non_contributives = simulation.calculate(
            'cotisations_employeur_non_contributives', period)
        cotisations_employeur_main_d_oeuvre = simulation.calculate('cotisations_employeur_main_d_oeuvre', period)

        return period, (
            cotisations_employeur_contributives +
            cotisations_employeur_non_contributives +
            cotisations_employeur_main_d_oeuvre
            )


@reference_formula
class cotisations_employeur_contributives(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales patronales contributives"
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        period = period
        ags = simulation.calculate('ags', period)
        agff_employeur = simulation.calculate_add('agff_employeur', period)
        apec_employeur = simulation.calculate('apec_employeur', period)
        arrco_employeur = simulation.calculate('arrco_employeur', period)
        chomage_employeur = simulation.calculate('chomage_employeur', period)
        cotisation_exceptionnelle_temporaire_employeur = simulation.calculate(
            'cotisation_exceptionnelle_temporaire_employeur', period)
        fonds_emploi_hospitalier = simulation.calculate_add('fonds_emploi_hospitalier', period)
        ircantec_employeur = simulation.calculate_add('ircantec_employeur', period)
        pension_civile_employeur = simulation.calculate_add('pension_civile_employeur', period)
        rafp_employeur = simulation.calculate_add('rafp_employeur', period)
        vieillesse_deplafonnee_employeur = simulation.calculate_add('vieillesse_deplafonnee_employeur', period)
        vieillesse_plafonnee_employeur = simulation.calculate_add('vieillesse_plafonnee_employeur', period)

        cotisations_employeur_contributives = (
            # prive
            ags +
            agff_employeur +
            apec_employeur +
            arrco_employeur +
            chomage_employeur +
            cotisation_exceptionnelle_temporaire_employeur +
            vieillesse_deplafonnee_employeur +
            vieillesse_plafonnee_employeur +
            # public
            fonds_emploi_hospitalier +
            ircantec_employeur +
            pension_civile_employeur +
            rafp_employeur
            )
        return period, cotisations_employeur_contributives


@reference_formula
class cotisations_employeur_non_contributives(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales patronales non-contributives"
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        period = period
        accident_du_travail = simulation.calculate_add('accident_du_travail', period)
        allocations_temporaires_invalidite = simulation.calculate_add('allocations_temporaires_invalidite', period)
        famille = simulation.calculate('famille', period)
        mmid_employeur = simulation.calculate_add('mmid_employeur', period)
        taxe_salaires = simulation.calculate_add('taxe_salaires', period)

        cotisations_employeur_non_contributives = (
            allocations_temporaires_invalidite +
            accident_du_travail +
            famille +
            mmid_employeur +
            taxe_salaires
            )
        return period, cotisations_employeur_non_contributives


@reference_formula
class cotisations_salariales_contributives(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales salariales contributives"
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        period = period
        agff_salarie = simulation.calculate_add('agff_salarie', period)
        agirc_salarie = simulation.calculate_add('agirc_salarie', period)
        apec_salarie = simulation.calculate_add('apec_salarie', period)
        arrco_salarie = simulation.calculate_add('arrco_salarie', period)
        chomage_salarie = simulation.calculate_add('chomage_salarie', period)
        cotisation_exceptionnelle_temporaire_salarie = simulation.calculate_add(
            'cotisation_exceptionnelle_temporaire_salarie', period)
        ircantec_salarie = simulation.calculate_add('ircantec_salarie', period)
        pension_civile_salarie = simulation.calculate_add('pension_civile_salarie', period)
        rafp_salarie = simulation.calculate_add('rafp_salarie', period)
        vieillesse_deplafonnee_salarie = simulation.calculate_add('vieillesse_deplafonnee_salarie', period)
        vieillesse_plafonnee_salarie = simulation.calculate_add('vieillesse_plafonnee_salarie', period)

        cotisations_salariales_contributives = (
            # prive
            agff_salarie +
            agirc_salarie +
            apec_salarie +
            arrco_salarie +
            chomage_salarie +
            cotisation_exceptionnelle_temporaire_salarie +
            vieillesse_deplafonnee_salarie +
            vieillesse_plafonnee_salarie +
            # public
            ircantec_salarie +
            pension_civile_salarie +
            rafp_salarie
            )

        return period, cotisations_salariales_contributives


@reference_formula
class cotisations_salariales_non_contributives(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales salariales non-contributives"
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        period = period
        contribution_exceptionnelle_solidarite = simulation.calculate_add(
            'contribution_exceptionnelle_solidarite', period)
        mmid_salarie = simulation.calculate_add('mmid_salarie', period)

        cotisations_salariales_non_contributives = (
            # prive
            mmid_salarie +
            # public
            contribution_exceptionnelle_solidarite
            )

        return period, cotisations_salariales_non_contributives


@reference_formula
class cotisations_salariales(SimpleFormulaColumn):
    base_function = requested_period_added_value
    column = FloatCol
    entity_class = Individus
    label = u"Cotisations sociales salariales"
    set_input = set_input_divide_by_period

    def function(self, simulation, period):
        period = period
        cotisations_salariales_contributives = simulation.calculate('cotisations_salariales_contributives', period)
        cotisations_salariales_non_contributives = simulation.calculate(
            'cotisations_salariales_non_contributives', period)

        return period, cotisations_salariales_contributives + cotisations_salariales_non_contributives
