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
    ccd=Namespace("http://this.ccd.com/")
    j=toc['medication-count']
    for i in range(1,j+1):
        meddata='medication-'+str(i)+'-data'
        med=toc[meddata]
        sub=ccd[meddata]
        g.add((sub,RDF.type,sp['Medication']))
        bto=ccd['medications']
        g.add((sub,sp['belongsTo'],bto))
        g.add((sub,sp['startDate'],Literal(p['effectiveTime'])))
        medname=BNode()
        g.add((sub,sp['medicationName'],medname))
        g.add((medname,RDF.type,sp['CodedValue']))
        g.add((medname,dcterms['title'],Literal(p['displayName'])))
        g.add((medname,sp['code'],snomed[p['code']]))
    return g

