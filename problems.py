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
from rdflib.URIRef import URIRef
from rdflib.constants import TYPE, VALUE

# Import RDFLib's default TripleStore implementation
from rdflib.TripleStore import TripleStore

def derive_problems(toc):
    j=toc['problem-count']
    for i in range(1,j+1):
        pname='problem-'+str(i)
        prob=toc[pname]
        toc[pname+'-data']=problem(toc,pname)
    return

def problem(toc,pname):
    p=toc[pname]
    g=p.find(".//{urn:hl7-org:v3}act/{urn:hl7-org:v3}entryRelationship/{urn:hl7-org:v3}observation/{urn:hl7-org:v3}value")
    data={}
    data['code']=g.attrib['code']
    data['codeSystemName']=g.attrib['codeSystemName']
    data['displayName']=g.attrib['displayName']
    g2=p.find(".//{urn:hl7-org:v3}act/{urn:hl7-org:v3}entryRelationship/{urn:hl7-org:v3}observation/{urn:hl7-org:v3}effectiveTime/{urn:hl7-org:v3}low")
    data['effectiveTime']=g2.attrib['value']
    g3=p.find(".//{urn:hl7-org:v3}act/{urn:hl7-org:v3}entryRelationship/{urn:hl7-org:v3}observation/{urn:hl7-org:v3}text/{urn:hl7-org:v3}reference")
    data['problemId']=g3.attrib['value']
    return data

def smart_problems(toc):
    g=rdflib.Graph()
    cdautil.rdfinit(g)
    # Create a namespace object
    dcterms=Namespace("http://purl.org/dc/terms/")
    rdf=Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    sp=Namespace("http://smartplatforms.org/terms#")
    smart=Namespace("http://sandbox-api.smartplatforms.org/records/")
    snomed=Namespace("http://purl.bioontology.org/ontology/SNOMEDCT/")
    ccd=Namespace("http://this.ccd.com/")
    j=toc['problem-count']
    for i in range(1,j+1):
        pdata='problem-'+str(i)+'-data'
        p=toc[pdata]
        sub=ccd[pdata]
        g.add((sub,RDF.type,sp['Problem']))
        bto=ccd['problems']
        g.add((sub,sp['belongsTo'],bto))
        g.add((sub,sp['startDate'],Literal(p['effectiveTime'])))
        probname=BNode()
        g.add((sub,sp['problemName'],probname))
        g.add((probname,RDF.type,sp['CodedValue']))
        g.add((probname,dcterms['title'],Literal(p['displayName'])))
        g.add((probname,sp['code'],snomed[p['code']]))
    return g

