#!/usr/bin/env python

# Copyright 2012 Author George Lilly (glilly at glilly dot net)
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

import xml.etree.ElementTree as ET
from rdflib import Literal, BNode, Namespace
from rdflib import RDF
import rdflib
#from rdflib.URIRef import URIRef
#from rdflib.constants import TYPE, VALUE

# Import RDFLib's default TripleStore implementation
#from rdflib.TripleStore import TripleStore


def rdfinit(g):
    # Create a namespace object
    dcterms=Namespace("http://purl.org/dc/terms/")
    rdf=Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    sp=Namespace("http://smartplatforms.org/terms#")
    smart=Namespace("http://sandbox-api.smartplatforms.org/records/")
    snomed=Namespace("http://purl.bioontology.org/ontology/SNOMEDCT/")
    ccd=Namespace("http://this.ccd.com/")
    g.bind("dcterms","http://purl.org/dc/terms/")
    g.bind("rdf","http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    g.bind("sp","http://smartplatforms.org/terms#")
    g.bind("smart","http://sandbox-api.smartplatforms.org/records/")
    g.bind("snomed","http://purl.bioontology.org/ontology/SNOMEDCT/")
    g.bind("ccd","http://this.ccd.com/")
    return g

def clean(gs):

    g = gs.replace('{urn:hl7-org:v3}','');
    return g

def clean2(gs):
    g = gs.replace('{http://www.w3.org/2001/XMLSchema-instance}','');
    return g

def sections(root):
    i={}
    x=0
    sec=root.findall(".//*{urn:hl7-org:v3}section")
    for cur in sec:
        x=x+1;
        if cur.find(".//{urn:hl7-org:v3}code/.[@code='10160-0']") != None:
            i['medications']=cur
            meds=0;
            e=cur.findall(".//{urn:hl7-org:v3}entry/")
            for entry in e:
                if entry.find(".//{urn:hl7-org:v3}templateId/.[@root='2.16.840.1.113883.10.20.1.24']") != None:
                    meds=meds+1;
                    i["medication-"+str(meds)]=entry
                i['medication-count']=meds
        elif cur.find(".//{urn:hl7-org:v3}code/.[@code='48765-2']") != None:
            i['allergies']=cur
            allergies=0;
            e=cur.findall(".//{urn:hl7-org:v3}entry/")
            for entry in e:
                if entry.find(".//{urn:hl7-org:v3}templateId/.[@root='2.16.840.1.113883.10.20.1.27']") != None:
                    allergies=allergies+1;
                    i["allergy-"+str(allergies)]=entry
                i['allergy-count']=allergies
        elif cur.find(".//{urn:hl7-org:v3}code/.[@code='30954-2']") != None:
            i['results']=cur
            results=0;
            e=cur.findall(".//{urn:hl7-org:v3}entry/")
            for entry in e:
                if entry.find(".//{urn:hl7-org:v3}templateId/.[@root='2.16.840.1.113883.10.20.1.32']") != None:
                    results=results+1;
                    i["results-"+str(results)]=entry
                i['results-count']=results
        elif cur.find(".//{urn:hl7-org:v3}code/.[@code='47519-4']") != None:
            i['procedures']=cur
            procedures=0;
            e=cur.findall(".//{urn:hl7-org:v3}entry/")
            for entry in e:
                if entry.find(".//{urn:hl7-org:v3}templateId/.[@root='2.16.840.1.113883.10.20.1.29']") != None:
                    procedures=procedures+1;
                    i["procedures-"+str(procedures)]=entry
                i['procedures-count']=procedures
        elif cur.find(".//{urn:hl7-org:v3}code/.[@code='11369-6']") != None:
            i['immune']=cur
            immune=0;
            e=cur.findall(".//{urn:hl7-org:v3}entry/")
            for entry in e:
                if entry.find(".//{urn:hl7-org:v3}templateId/.[@root='2.16.840.1.113883.10.20.1.24']") != None:
                    immune=immune+1;
                    i["immunization-"+str(immune)]=entry
                i['immunization-count']=immune
        elif cur.find(".//{urn:hl7-org:v3}code/.[@code='11450-4']") != None:
            i['problems']=cur
            probs=0;
            e=cur.findall(".//{urn:hl7-org:v3}entry")
            for entry in e:
                if entry.find(".//{urn:hl7-org:v3}templateId/.[@root='2.16.840.1.113883.10.20.1.27']") != None:
                    probs=probs+1;
                    i["problem-"+str(probs)]=entry
                i["problem-count"]=probs
        else :
            i['unknown'+str(x)]=cur;
    return i

