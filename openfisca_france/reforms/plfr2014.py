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

import copy
from datetime import date

import logging

from numpy import maximum as max_, minimum as min_
from openfisca_core import columns, formulas, reforms

from .. import entities
from ..model import base
from ..model.prelevements_obligatoires.impot_revenu import reductions_impot


log = logging.getLogger(__name__)


# TODO: les baisses de charges n'ont pas été codées car annulées (toute ou en partie ?)
# par le Conseil constitutionnel


# Reform formulas

class reduction_impot_exceptionnelle(formulas.SimpleFormulaColumn):
    column = columns.FloatCol
    entity_class = entities.FoyersFiscaux
    label = u"Réduction d'impôt exceptionnelle"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        nb_adult = simulation.calculate('nb_adult')
        nb_par = simulation.calculate('nb_par')
        rfr = simulation.calculate('rfr')
        params = simulation.legislation_at(period.start).plfr2014.reduction_impot_exceptionnelle
        plafond = params.seuil * nb_adult + (nb_par - nb_adult) * 2 * params.majoration_seuil
        montant = params.montant_plafond * nb_adult
        return period, min_(max_(plafond + montant - rfr, 0), montant)


class reductions(formulas.DatedFormulaColumn):
    label = u"Somme des réductions d'impôt à intégrer pour l'année 2013"
    reference = reductions_impot.reductions

    @base.dated_function(start = date(2013, 1, 1), stop = date(2013, 12, 31))
    def function_20130101_20131231(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        accult = simulation.calculate('accult')
        adhcga = simulation.calculate('adhcga')
        cappme = simulation.calculate('cappme')
        creaen = simulation.calculate('creaen')
        daepad = simulation.calculate('daepad')
        deffor = simulation.calculate('deffor')
        dfppce = simulation.calculate('dfppce')
        doment = simulation.calculate('doment')
        domlog = simulation.calculate('domlog')
        donapd = simulation.calculate('donapd')
        duflot = simulation.calculate('duflot')
        ecpess = simulation.calculate('ecpess')
        garext = simulation.calculate('garext')
        intagr = simulation.calculate('intagr')
        invfor = simulation.calculate('invfor')
        invlst = simulation.calculate('invlst')
        ip_net = simulation.calculate('ip_net')
        locmeu = simulation.calculate('locmeu')
        mecena = simulation.calculate('mecena')
        mohist = simulation.calculate('mohist')
        patnat = simulation.calculate('patnat')
        prcomp = simulation.calculate('prcomp')
        reduction_impot_exceptionnelle = simulation.calculate('reduction_impot_exceptionnelle')
        repsoc = simulation.calculate('repsoc')
        resimm = simulation.calculate('resimm')
        rsceha = simulation.calculate('rsceha')
        saldom = simulation.calculate('saldom')
        scelli = simulation.calculate('scelli')
        sofica = simulation.calculate('sofica')
        spfcpi = simulation.calculate('spfcpi')
        total_reductions = accult + adhcga + cappme + creaen + daepad + deffor + dfppce + doment + domlog + donapd + \
            duflot + ecpess + garext + intagr + invfor + invlst + locmeu + mecena + mohist + patnat + prcomp + \
            repsoc + resimm + rsceha + saldom + scelli + sofica + spfcpi + reduction_impot_exceptionnelle
        return period, min_(ip_net, total_reductions)


# Reform legislation

reform_legislation_subtree = {
    "plfr2014": {
        "@type": "Node",
        "description": "Projet de loi de finance rectificative 2014",
        "children": {
            "reduction_impot_exceptionnelle": {
                "@type": "Node",
                "description": "Réduction d'impôt exceptionnelle",
                "children": {
                    "montant_plafond": {
                        "@type": "Parameter",
                        "description": "Montant plafond par part pour les deux premières parts",
                        "format": "integer",
                        "unit": "currency",
                        "values": [{'start': u'2013-01-01', 'stop': u'2014-12-31', 'value': 350}],
                        },
                    "seuil": {
                        "@type": "Parameter",
                        "description": "Seuil (à partir duquel la réduction décroît) par part pour les deux "
                                       "premières parts",
                        "format": "integer",
                        "unit": "currency",
                        "values": [{'start': u'2013-01-01', 'stop': u'2014-12-31', 'value': 13795}],
                        },
                    "majoration_seuil": {
                        "@type": "Parameter",
                        "description": "Majoration du seuil par demi-part supplémentaire",
                        "format": "integer",
                        "unit": "currency",
                        "values": [{'start': u'2013-01-01', 'stop': u'2014-12-31', 'value': 3536}],
                        },
                    },
                },
            },
        },
    "plfrss2014": {
        "@type": "Node",
        "description": "Projet de loi de financement de la sécurité sociale rectificative 2014",
        "children": {
            "exonerations_bas_salaires": {
                "@type": "Node",
                "description": "Exonérations de cotisations salariées sur les bas salaires",
                "children": {
                    "prive": {
                        "@type": "Node",
                        "description": "Salariés du secteur privé",
                        "children": {
                            "taux": {
                                "@type": "Parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.03}],
                                },
                            "seuil": {
                                "@type": "Parameter",
                                "description": "Seuil (en SMIC)",
                                "format": "rate",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 1.3}],
                                },
                            },
                        },
                    "public": {
                        "@type": "Node",
                        "description": "Salariés du secteur public",
                        "children": {
                            "taux_1": {
                                "@type": "Parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.02}],
                                },
                            "seuil_1": {
                                "@type": "Parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 312}],
                                },
                            "taux_2": {
                                "@type": "Parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.018}],
                                },
                            "seuil_2": {
                                "@type": "Parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 328}],
                                },
                            "taux_3": {
                                "@type": "Parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.016}],
                                },
                            "seuil_3": {
                                "@type": "Parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 343}],
                                },
                            "taux_4": {
                                "@type": "Parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.014}],
                                },
                            "seuil_4": {
                                "@type": "Parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 359}],
                                },
                            "taux_5": {
                                "@type": "Parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.012}],
                                },
                            "seuil_5": {
                                "@type": "Parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 375}],
                                },
                            "taux_6": {
                                "@type": "Parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.01}],
                                },
                            "seuil_6": {
                                "@type": "Parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 390}],
                                },
                            "taux_7": {
                                "@type": "Parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.008}],
                                },
                            "seuil_7": {
                                "@type": "Parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 406}],
                                },
                            "taux_8": {
                                "@type": "Parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.007}],
                                },
                            "seuil_8": {
                                "@type": "Parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 421}],
                                },
                            "taux_9": {
                                "@type": "Parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.006}],
                                },
                            "seuil_9": {
                                "@type": "Parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 437}],
                                },
                            "taux_10": {
                                "@type": "Parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.005}],
                                },
                            "seuil_10": {
                                "@type": "Parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 453}],
                                },
                            "taux_11": {
                                "@type": "Parameter",
                                "description": "Taux",
                                "format": "rate",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 0.002}],
                                },
                            "seuil_11": {
                                "@type": "Parameter",
                                "description": "Indice majoré plafond",
                                "format": "integer",
                                "values": [{'start': u'2014-01-01', 'stop': u'2014-12-31', 'value': 468}],
                                },
                            },
                        },
                    },
                },
            },
        },
    }


# Build function

def build_reform(tax_benefit_system):
    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = copy.deepcopy(reference_legislation_json)
    reform_legislation_json['children'].update(reform_legislation_subtree)
    Reform = reforms.make_reform(
        legislation_json = reform_legislation_json,
        name = u'PLFR 2014',
        new_formulas = (reduction_impot_exceptionnelle, reductions),
        reference = tax_benefit_system,
        )
    return Reform()
