cdadiet
=======

python (and maybe other) tool framework for processing cda xml documents. will yield smart rdf and other formats. 

current output printed from a sample CCD:
<pre>
@glilly:~/cdadiet$ python cdadiet.py
@prefix ccd: <http://this.ccd.com/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix sp: <http://smartplatforms.org/terms#> .

ccd:problem-1-data a sp:Problem;
    sp:belongsTo ccd:problems;
    sp:problemName [ a sp:CodedValue;
            dcterms:title "Diabetes Mellitus, Type 2";
            sp:code <http://purl.bioontology.org/ontology/SNOMEDCT/44054006> ];
    sp:startDate "2009" .

ccd:problem-2-data a sp:Problem;
    sp:belongsTo ccd:problems;
    sp:problemName [ a sp:CodedValue;
            dcterms:title "Hyperlipidemia";
            sp:code <http://purl.bioontology.org/ontology/SNOMEDCT/55822004> ];
    sp:startDate "200205" .

ccd:problem-3-data a sp:Problem;
    sp:belongsTo ccd:problems;
    sp:problemName [ a sp:CodedValue;
            dcterms:title "Coronary Arteriosclerosis";
            sp:code <http://purl.bioontology.org/ontology/SNOMEDCT/53741008> ];
    sp:startDate "200205" .

ccd:problem-4-data a sp:Problem;
    sp:belongsTo ccd:problems;
    sp:problemName [ a sp:CodedValue;
            dcterms:title "Essential Hypertension";
            sp:code <http://purl.bioontology.org/ontology/SNOMEDCT/59621000> ];
    sp:startDate "200205" .

@prefix ccd: <http://this.ccd.com/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix sp: <http://smartplatforms.org/terms#> .

ccd:medication-1-data a sp:Medication;
    sp:belongsTo ccd:medications;
    sp:medicationName [ a sp:CodedValue;
            dcterms:title "glyburide 2.5 mg Oral Tablet (Diabeta)";
            sp:code <http://purl.bioontology.org/ontology/RXNORM/205875>;
            sp:frequency [ sp:unit "h";
                    sp:value "24" ];
            sp:instructions [ sp:route [ a sp:CodedValue;
                            dcterms:title "Oral";
                            sp:code "C38288";
                            sp:codeSystemName "FDA RouteOfAdministration" ] ];
            sp:quantity [ sp:unit "tablet";
                    sp:value "1" ] ];
    sp:startDate "20090916" .

ccd:medication-2-data a sp:Medication;
    sp:belongsTo ccd:medications;
    sp:medicationName [ a sp:CodedValue;
            dcterms:title "atorvastatin calcium 10 mg Oral Tablet (Lipitor)";
            sp:code <http://purl.bioontology.org/ontology/RXNORM/617314>;
            sp:frequency [ sp:unit "h";
                    sp:value "24" ];
            sp:instructions [ sp:route [ a sp:CodedValue;
                            dcterms:title "Swallow, oral";
                            sp:code "PO";
                            sp:codeSystemName "HL7 RouteOfAdministration" ] ];
            sp:quantity [ sp:unit "tablet";
                    sp:value "1" ] ];
    sp:startDate "20020505" .

ccd:medication-3-data a sp:Medication;
    sp:belongsTo ccd:medications;
    sp:medicationName [ a sp:CodedValue;
            dcterms:title "Furosemide 20 MG Oral Tablet [Lasix]";
            sp:code <http://purl.bioontology.org/ontology/RXNORM/200801>;
            sp:frequency [ sp:unit "h";
                    sp:value "12" ];
            sp:instructions [ sp:route [ a sp:CodedValue;
                            dcterms:title "Swallow, oral";
                            sp:code "PO";
                            sp:codeSystemName "HL7 RouteOfAdministration" ] ];
            sp:quantity [ sp:unit "tablet";
                    sp:value "1" ] ];
    sp:startDate "20020505" .

ccd:medication-4-data a sp:Medication;
    sp:belongsTo ccd:medications;
    sp:medicationName [ a sp:CodedValue;
            dcterms:title "potassium chloride 10 mEq Oral Tablet (Klor-Con)";
            sp:code <http://purl.bioontology.org/ontology/RXNORM/628958>;
            sp:frequency [ sp:unit "h";
                    sp:value "12" ];
            sp:instructions [ sp:route [ a sp:CodedValue;
                            dcterms:title "Swallow, oral";
                            sp:code "PO";
                            sp:codeSystemName "HL7 RouteOfAdministration" ] ];
            sp:quantity [ sp:unit "tablet";
                    sp:value "1" ] ];
    sp:startDate "20020505" .
</pre>
