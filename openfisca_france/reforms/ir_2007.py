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
from ..model.prelevements_obligatoires.impot_revenu import ir


log = logging.getLogger(__name__)


# TODO: les baisses de charges n'ont pas été codées car annulées (toute ou en partie ?)
# par le Conseil constitutionnel


# Reform formulas

class ir_brut(formulas.SimpleFormulaColumn):
    label = u"ir_brut"
    reference = ir.ir_brut

    def function(self, simulation, period):
        '''
        Impot sur le revenu avant non imposabilité et plafonnement du quotient
        'foy'
        '''
        period = period.start.offset('first-of', 'month').period('year')
        nbptr = simulation.calculate('nbptr', period)
        taux_effectif = simulation.calculate('taux_effectif', period)
        rni = simulation.calculate('rni', period)
        bareme = simulation.legislation_at(period.start).ir.bareme


        return period, (taux_effectif == 0) * nbptr * bareme.calc(rni / nbptr) + taux_effectif * rni

  <NODE code="ir" description="Impôt sur le revenu">
    <BAREME code="bareme" description="Tranches de l'IR" type="monetary">
      <TRANCHE code="tranche0">
        <SEUIL>
          <VALUE deb="2001-01-01" fin="2014-12-31" valeur="0" />
        </SEUIL>
        <TAUX>
          <VALUE deb="2001-01-01" fin="2014-12-31" valeur="0" />
        </TAUX>
      </TRANCHE>
      <TRANCHE code="tranche1">
        <SEUIL>
          <VALUE deb="2001-01-01" fin="2001-12-31" valeur="4121" />
          <VALUE deb="2002-01-01" fin="2002-12-31" valeur="4191" />
          <VALUE deb="2003-01-01" fin="2003-12-31" valeur="4262" />
          <VALUE deb="2004-01-01" fin="2004-12-31" valeur="4334" />
          <VALUE deb="2005-01-01" fin="2005-12-31" valeur="4412" />
          <VALUE deb="2006-01-01" fin="2006-12-31" valeur="5614" />
          <VALUE deb="2007-01-01" fin="2007-12-31" valeur="5687" />
          <VALUE deb="2008-01-01" fin="2008-12-31" valeur="5852" />
          <VALUE deb="2009-01-01" fin="2009-12-31" valeur="5875" />
          <VALUE deb="2010-01-01" fin="2012-12-31" valeur="5963" />
          <VALUE deb="2013-01-01" fin="2013-12-31" valeur="6011" />
          <VALUE deb="2014-01-01" fin="2014-12-31" valeur="9690" />
        </SEUIL>
        <TAUX>
          <VALUE deb="2001-01-01" fin="2002-12-31" valeur="0.0705" />
          <VALUE deb="2003-01-01" fin="2005-12-31" valeur="0.0683" />
          <VALUE deb="2006-01-01" fin="2013-12-31" valeur="0.055" />
          <VALUE deb="2014-01-01" fin="2014-12-31" valeur="0.14" />
        </TAUX>
      </TRANCHE>
      <TRANCHE code="tranche2">
        <SEUIL>
          <VALUE deb="2001-01-01" fin="2001-12-31" valeur="8104" />
          <VALUE deb="2002-01-01" fin="2002-12-31" valeur="8242" />
          <VALUE deb="2003-01-01" fin="2003-12-31" valeur="8382" />
          <VALUE deb="2004-01-01" fin="2004-12-31" valeur="8524" />
          <VALUE deb="2005-01-01" fin="2005-12-31" valeur="8677" />
          <VALUE deb="2006-01-01" fin="2006-12-31" valeur="11198" />
          <VALUE deb="2007-01-01" fin="2007-12-31" valeur="11344" />
          <VALUE deb="2008-01-01" fin="2008-12-31" valeur="11673" />
          <VALUE deb="2009-01-01" fin="2009-12-31" valeur="11720" />
          <VALUE deb="2010-01-01" fin="2012-12-31" valeur="11896" />
          <VALUE deb="2013-01-01" fin="2013-12-31" valeur="11991" />
          <VALUE deb="2014-01-01" fin="2014-12-31" valeur="26764" />
        </SEUIL>
        <TAUX>
          <VALUE deb="2001-01-01" fin="2001-12-31" valeur="0.21" />
          <VALUE deb="2002-01-01" fin="2005-12-31" valeur="0.1914" />
          <VALUE deb="2006-01-01" fin="2013-12-31" valeur="0.14" />
          <VALUE deb="2014-01-01" fin="2014-12-31" valeur="0.30" />
        </TAUX>
      </TRANCHE>
      <TRANCHE code="tranche3">
        <SEUIL>
          <VALUE deb="2001-01-01" fin="2001-12-31" valeur="14264" />
          <VALUE deb="2002-01-01" fin="2002-12-31" valeur="14506" />
          <VALUE deb="2003-01-01" fin="2003-12-31" valeur="14753" />
          <VALUE deb="2004-01-01" fin="2004-12-31" valeur="15004" />
          <VALUE deb="2005-01-01" fin="2005-12-31" valeur="15274" />
          <VALUE deb="2006-01-01" fin="2006-12-31" valeur="24872" />
          <VALUE deb="2007-01-01" fin="2007-12-31" valeur="25195" />
          <VALUE deb="2008-01-01" fin="2008-12-31" valeur="25926" />
          <VALUE deb="2009-01-01" fin="2009-12-31" valeur="26030" />
          <VALUE deb="2010-01-01" fin="2012-12-31" valeur="26420" />
          <VALUE deb="2013-01-01" fin="2013-12-31" valeur="26631" />
          <VALUE deb="2014-01-01" fin="2014-12-31" valeur="71754" />
        </SEUIL>
        <TAUX>
          <VALUE deb="2001-01-01" fin="2001-12-31" valeur="0.3100" />
          <VALUE deb="2002-01-01" fin="2002-12-31" valeur="0.2914" />
          <VALUE deb="2003-01-01" fin="2005-12-31" valeur="0.2826" />
          <VALUE deb="2006-01-01" fin="2013-12-31" valeur="0.3000" />
          <VALUE deb="2014-01-01" fin="2014-12-31" valeur="0.4100" />
        </TAUX>
      </TRANCHE>
      <TRANCHE code="tranche4">
        <SEUIL>
          <VALUE deb="2001-01-01" fin="2001-12-31" valeur="23096" />
          <VALUE deb="2002-01-01" fin="2002-12-31" valeur="23489" />
          <VALUE deb="2003-01-01" fin="2003-12-31" valeur="23888" />
          <VALUE deb="2004-01-01" fin="2004-12-31" valeur="24294" />
          <VALUE deb="2005-01-01" fin="2005-12-31" valeur="24731" />
          <VALUE deb="2006-01-01" fin="2006-12-31" valeur="66679" />
          <VALUE deb="2007-01-01" fin="2007-12-31" valeur="67546" />
          <VALUE deb="2008-01-01" fin="2008-12-31" valeur="69505" />
          <VALUE deb="2009-01-01" fin="2009-12-31" valeur="69783" />
          <VALUE deb="2010-01-01" fin="2012-12-31" valeur="70830" />
          <VALUE deb="2013-01-01" fin="2013-12-31" valeur="71397" />
          <VALUE deb="2014-01-01" fin="2014-12-31" valeur="151956" />
        </SEUIL>
        <TAUX>
          <VALUE deb="2001-01-01" fin="2001-12-31" valeur="0.4100" />
          <VALUE deb="2002-01-01" fin="2002-12-31" valeur="0.3854" />
          <VALUE deb="2003-01-01" fin="2005-12-31" valeur="0.3738" />
          <VALUE deb="2006-01-01" fin="2009-12-31" valeur="0.4000" />
          <VALUE deb="2010-01-01" fin="2013-12-31" valeur="0.4100" />
          <VALUE deb="2014-01-01" fin="2014-12-31" valeur="0.4500" />
        </TAUX>
      </TRANCHE>
      <TRANCHE code="tranche5">
        <SEUIL>
          <VALUE deb="2001-01-01" fin="2001-12-31" valeur="37579" />
          <VALUE deb="2002-01-01" fin="2002-12-31" valeur="38218" />
          <VALUE deb="2003-01-01" fin="2003-12-31" valeur="38868" />
          <VALUE deb="2004-01-01" fin="2004-12-31" valeur="39529" />
          <VALUE deb="2005-01-01" fin="2005-12-31" valeur="40241" />
          <VALUE deb="2012-01-01" fin="2012-12-31" valeur="150000" />
          <VALUE deb="2013-01-01" fin="2013-12-31" valeur="151200" />
        </SEUIL>
        <TAUX>
          <VALUE deb="2001-01-01" fin="2001-12-31" valeur="0.4675" />
          <VALUE deb="2002-01-01" fin="2002-12-31" valeur="0.4394" />
          <VALUE deb="2003-01-01" fin="2005-12-31" valeur="0.4262" />
          <VALUE deb="2012-01-01" fin="2013-12-31" valeur="0.4500" />
        </TAUX>
      </TRANCHE>
      <TRANCHE code="tranche6">
        <SEUIL>
          <VALUE deb="2001-01-01" fin="2001-12-31" valeur="46343" />
          <VALUE deb="2002-01-01" fin="2002-12-31" valeur="47131" />
          <VALUE deb="2003-01-01" fin="2003-12-31" valeur="47932" />
          <VALUE deb="2004-01-01" fin="2004-12-31" valeur="48747" />
          <VALUE deb="2005-01-01" fin="2005-12-31" valeur="49624" />
        </SEUIL>
        <TAUX>
          <VALUE deb="2001-01-01" fin="2001-12-31" valeur="0.5275" />
          <VALUE deb="2002-01-01" fin="2002-12-31" valeur="0.4958" />
          <VALUE deb="2003-01-01" fin="2005-12-31" valeur="0.4809" />
        </TAUX>
      </TRANCHE>

# Reform legislation
OrderedDict([(
    '@type', 'Scale'),
    ('unit', u'currency'),
    ('description', "Tranches de l'IR"),
    ('brackets',[
        OrderedDict([
            ('threshold', [OrderedDict([('start', u'2001-01-01'), ('stop', u'2014-12-31'), ('value', 0.0)])]),
            ('rate', [OrderedDict([('start', u'2001-01-01'), ('stop', u'2014-12-31'), ('value', 0.0)])])]),
        OrderedDict([
            ('threshold', [
                        OrderedDict([('start', u'2014-01-01'), ('stop', u'2014-12-31'), ('value', 9690.0)]),
                        OrderedDict([('start', u'2013-01-01'), ('stop', u'2013-12-31'), ('value', 6011.0)]),
                        OrderedDict([('start', u'2010-01-01'), ('stop', u'2012-12-31'), ('value', 5963.0)]),
                        OrderedDict([('start', u'2009-01-01'), ('stop', u'2009-12-31'), ('value', 5875.0)]),
                        OrderedDict([('start', u'2008-01-01'), ('stop', u'2008-12-31'), ('value', 5852.0)]),
                        OrderedDict([('start', u'2007-01-01'), ('stop', u'2007-12-31'), ('value', 5687.0)]),
                        OrderedDict([('start', u'2006-01-01'), ('stop', u'2006-12-31'), ('value', 5614.0)]),
                        OrderedDict([('start', u'2005-01-01'), ('stop', u'2005-12-31'), ('value', 4412.0)]),
                        OrderedDict([('start', u'2004-01-01'), ('stop', u'2004-12-31'), ('value', 4334.0)]),
                        OrderedDict([('start', u'2003-01-01'), ('stop', u'2003-12-31'), ('value', 4262.0)]),
                        OrderedDict([('start', u'2002-01-01'), ('stop', u'2002-12-31'), ('value', 4191.0)]),
                        OrderedDict([('start', u'2001-01-01'), ('stop', u'2001-12-31'), ('value', 4121.0)])]),
            ('rate', [OrderedDict([('start', u'2014-01-01'), ('stop', u'2014-12-31'), ('value', 0.14)]),

reform_legislation_subtree = {
    "ir_2007": {
        "@type": "Node",
        "description": "",
        "children": {
            "ir_2007": {
                "@type": "Scale",
                "unit": "currency",
                "description": "Tranches",
                "brackets": {
                    "threshold": [{'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 0.0}],
                    "rate": [{'start': u'2007-01-01', 'stop': u'2007-12-31', 'value': 0.0}],
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
tax_benefit_system.legislation_json['children']['ir']['children']['bareme']

def build_reform(tax_benefit_system):
    reference_legislation_json = tax_benefit_system.legislation_json
    reform_legislation_json = copy.deepcopy(reference_legislation_json)
    reform_legislation_json['children'].update(reform_legislation_subtree)
    Reform = reforms.make_reform(
        legislation_json = reform_legislation_json,
        name = u'impot sur le revenu 2007',
        new_formulas = (reduction_impot_exceptionnelle, reductions),
        reference = tax_benefit_system,
        )
    return Reform()
