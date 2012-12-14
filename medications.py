#!/usr/bin/env python

# Copyright 2012 Author
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
import cdautil
import xml.etree.ElementTree as ET
from rdflib import Literal, BNode, Namespace
from rdflib import RDF
import rdflib
#from rdflib.URIRef import URIRef
#from rdflib.constants import TYPE, VALUE

# Import RDFLib's default TripleStore implementation
#from rdflib.TripleStore import TripleStore

def derive_medications(toc):
    j=toc['medication-count']
    for i in range(1,j+1):
        medname='medication-'+str(i)
        med=toc[medname]
        toc[medname+'-data']=medication(toc,medname)
    return

def medication(toc,medname):
    med=toc[medname]
    g=med.find(".//{urn:hl7-org:v3}consumable/{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}manufacturedMaterial/{urn:hl7-org:v3}code")
#    print g
#    print g.attrib
    data={}
    data['code']=g.attrib['code']
    data['codeSystemName']=g.attrib['codeSystemName']
    data['displayName']=g.attrib['displayName']
    g2=med.find(".//{urn:hl7-org:v3}consumable/{urn:hl7-org:v3}manufacturedProduct/{urn:hl7-org:v3}manufacturedMaterial/{urn:hl7-org:v3}name")
    data['name']=g2.text
    route={}
    r=med.find(".//{urn:hl7-org:v3}routeCode")
    route['code']=r.attrib['code']
    route['codeSystemName']=r.attrib['codeSystemName']
    route['displayName']=r.attrib['displayName']
    route['codeSystem']=r.attrib['codeSystem']
    r2=med.find(".//{urn:hl7-org:v3}routeCode/{urn:hl7-org:v3}originalText")
    if (r2 is not None):
        route['originalText']=r2.text
    r3=med.find(".//{urn:hl7-org:v3}routeCode/{urn:hl7-org:v3}translation")
    if (r3 is not None):
        rtcde={}
        rtcde['code']=r3.attrib['code']
        rtcde['codeSystem']=r3.attrib['codeSystem']
        rtcde['displayName']=r3.attrib['displayName']
        rtcde['codeSystemName']=r3.attrib['codeSystemName']
        route['translation']=rtcde
    data['route']=route
    d1=med.find(".//{urn:hl7-org:v3}doseQuantity")
    dose={}
    dose['value']=d1.attrib['value']
    dose['unit']=d1.attrib['unit']
    data['dose']=dose
    t1=med.find(".//{urn:hl7-org:v3}effectiveTime/{urn:hl7-org:v3}low")
    data['effectiveTime']=t1.attrib['value']
    period={}
    t2=med.find(".//{urn:hl7-org:v3}effectiveTime/{urn:hl7-org:v3}period")
    period['value']=t2.attrib['value']
    period['unit']=t2.attrib['unit']
    data['period']=period
    return data
#    g2=p.find(".//{urn:hl7-org:v3}act/{urn:hl7-org:v3}entryRelationship/{urn:hl7-org:v3}observation/{urn:hl7-org:v3}effectiveTime/{urn:hl7-org:v3}low")
#    data['effectiveTime']=g2.attrib['value']
#    g3=p.find(".//{urn:hl7-org:v3}act/{urn:hl7-org:v3}entryRelationship/{urn:hl7-org:v3}observation/{urn:hl7-org:v3}text/{urn:hl7-org:v3}reference")
#    data['problemId']=g3.attrib['value']


def smart_medications(toc):
    g=rdflib.Graph()
    cdautil.rdfinit(g)
    # Create a namespace object
    dcterms=Namespace("http://purl.org/dc/terms/")
    rdf=Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    sp=Namespace("http://smartplatforms.org/terms#")
    smart=Namespace("http://sandbox-api.smartplatforms.org/records/")
    snomed=Namespace("http://purl.bioontology.org/ontology/SNOMEDCT/")
    rxnorm=Namespace("http://purl.bioontology.org/ontology/RXNORM/")
    ccd=Namespace("http://this.ccd.com/")
    j=toc['medication-count']
    for i in range(1,j+1):
        meddata='medication-'+str(i)+'-data'
        med=toc[meddata]
        sub=ccd[meddata]
        g.add((sub,RDF.type,sp['Medication']))
        bto=ccd['medications']
        g.add((sub,sp['belongsTo'],bto))
        g.add((sub,sp['startDate'],Literal(med['effectiveTime'])))
        medname=BNode()
        g.add((sub,sp['medicationName'],medname))
        g.add((medname,RDF.type,sp['CodedValue']))
        g.add((medname,dcterms['title'],Literal(med['displayName'])))
        g.add((medname,sp['code'],rxnorm[med['code']]))
        route=med['route']
        binstr=BNode()
        broute=BNode()
        g.add((medname,sp['instructions'],binstr))
        g.add((binstr,sp['route'],broute))
        g.add((broute,RDF.type,sp['CodedValue']))
        g.add((broute,sp['codeSystemName'],Literal(route['codeSystemName'])))
        g.add((broute,sp['code'],Literal(route['code'])))
        g.add((broute,dcterms['title'],Literal(route['displayName'])))
#        g.add((broute,sp['originalText'],Literal(route['originalText'])))
#        try rtrans=route['translation']
#        brtrans=BNode()
#        g.add((broute,sp['translation'],brtrans))
#        g.add((brtrans,RDF.type,sp['CodedValue']))
#        g.add((brtrans,sp['codeSystemName'],Literal(rtrans['codeSystemName'])))
#        g.add((brtrans,sp['code'],Literal(rtrans['code'])))
#        g.add((brtrans,dcterms['title'],Literal(rtrans['displayName'])))
        period=med['period']
        bperiod=BNode()
        dose=med['dose']
        bdose=BNode()
        g.add((medname,sp['quantity'],bdose))
        g.add((bdose,sp['unit'],Literal(dose['unit'])))
        g.add((bdose,sp['value'],Literal(dose['value'])))
        freq=med['period']
        bfreq=BNode()
        g.add((medname,sp['frequency'],bfreq))
#        g.add((bfreq,RDF.type,sp['CodedValue']))
        g.add((bfreq,sp['unit'],Literal(freq['unit'])))
        g.add((bfreq,sp['value'],Literal(freq['value'])))
    return g

