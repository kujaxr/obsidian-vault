# nokia.pdf

 
Verification Methods Of 
Materials 
 
1 (90) 
DQD/TQ, Device R&D 
 
 
 
 
17.12.2009 
Confidential 1H2010 release 
 
 
 
 
 
 
 
 
 
 
TEST SPECIFICATION FOR MATERIALS 
(1H2010 release) 
 
 
 
 
 
 
 
Copyright © Nokia Corporation. This material, including documentation and any 
related computer programs, is protected by copyright controlled by Nokia 
Corporation. All rights are reserved. Copying, including reproducing, storing, 
adapting or translating, any or all of this material requires the prior written 
consent of Nokia Corporation. This material also contains confidential 
information, which may not be disclosed to others without the prior written 
consent of Nokia Corporation. 
 
 
 
 
 
 
 
 
 
 
 
 
 
 


 
Verification Methods Of 
Materials 
 
2 (90) 
DQD/TQ, Device R&D 
 
 
 
 
17.12.2009 
Confidential 1H2010 release 
 
 
TABLE OF CONTENTS 
 
1. 
INTRODUCTIONS ......................................................................................................................... 4 
1.1 
Scope ...................................................................................................................................... 4 
1.2 
Abbreviations........................................................................................................................... 4 
1.3 
Definitions................................................................................................................................ 5 
2. 
MEASUREMENTS......................................................................................................................... 7 
2.1 
Visual....................................................................................................................................... 7 
2.1.1 
Visual inspection .............................................................................................................. 7 
2.2 
Mechanical .............................................................................................................................. 9 
2.2.1 
Residual Stress ................................................................................................................ 9 
2.2.2 
Surface roughness (Rq) ................................................................................................. 11 
2.2.3 
Surface waviness ........................................................................................................... 11 
2.2.4 
Coating thickness measurements .................................................................................. 11 
2.2.5 
Adhesion strength of tapes............................................................................................. 13 
2.3 
Electrical................................................................................................................................ 16 
2.3.1 
Electric resistance .......................................................................................................... 16 
2.4 
Optical ................................................................................................................................... 17 
2.4.1 
Transparency (transmittance / transmissivity)................................................................ 17 
2.4.2 
Haze............................................................................................................................... 21 
2.4.3 
Birefringence (phase delay between polarizations)........................................................ 23 
2.4.4 
Gloss .............................................................................................................................. 26 
2.4.5 
Color measurement........................................................................................................ 29 
3. 
TESTS.......................................................................................................................................... 31 
3.1 
Mechanical tests.................................................................................................................... 31 
3.1.1 
Adhesion test for coated surfaces .................................................................................. 31 
3.1.2 
Vibratory wearing ........................................................................................................... 35 
3.1.3 
Disk wearing test ............................................................................................................ 40 
3.1.4 
Sand Abrasion Test........................................................................................................ 44 
3.1.5 
Rod test.......................................................................................................................... 46 
3.1.6 
Guided free fall test ........................................................................................................ 48 
3.1.7 
Repeated free fall........................................................................................................... 51 
3.1.8 
Ball Drop Test................................................................................................................. 53 
3.1.9 
Impact Hammer Test...................................................................................................... 56 
3.1.10 
Safety force test.......................................................................................................... 58 
3.1.11 
Denim test................................................................................................................... 60 
3.2 
Thermal ................................................................................................................................. 64 
3

 
Verification Methods Of 
Materials 
 
3 (90) 
DQD/TQ, Device R&D 
 
 
 
 
17.12.2009 
Confidential 1H2010 release 
 
 
 


 
Verification Methods Of 
Materials 
 
4 (90) 
DQD/TQ, Device R&D 
 
 
 
 
17.12.2009 
Confidential 1H2010 release 
 
 
1. INTRODUCTIONS 
1.1 Scope  
This document describes the test methods and procedures used for technology 
development / verification of materials. Its scope is for module / component level testing 
only and must not be used as the requirements for product level verification. 
This document is primerily focused on the test methods and procedures and not the 
acceptance criteria. It is normal for acceptance criteria to be described in standard 
technology requirements (STR) of materials or in project / product specifications or other 
related documents. In the event of conflict between the STR and project / product 
specifications, the requirements in project / product specifications (or other related 
documents) shall be followed.  
The test methods listed in this document cover several technology areas and it is the 
responsibilities of development professionals to determine which tests (measurements) 
are applicable for the individual technology area. 
The documents referenced in each section can be used for clarification of methods or as 
a source of supporting information. However, in the event of conflict between this and 
the reference documents the requirements of this document shall be followed in all 
cases. 
In the evet that project / product have unique requirements contrary to the tests listed 
herein, they will be considered as customised test cases, the methods and procedures 
given in this document are no longer valid. The project / product who initiated the custom 
test case will have the responsibility to provide and document for the test procedure. 
This document is intended for Nokia internal use only; however if it is required for 
delivery third to a third party for co-development work or quality / process control it must 
be rewritten in accordance with the officail NDA and delivered in part or whole. It is the 
responsibility of the individual sending the document to check that it conforms to the 
official NDA policy. 
1.2 Abbreviations 
ASTM: American Society for Testing and Materials standards 
CIE: Internal Commission on Illumination 
D/0: Optical system configuration defined by CIE, Diffusion / normal (0 degree to the 
normal of surface) 
DI: Deionized 
IEC: International Electrotechnical Commission 
ISO: International Organization for Standardization 
NDA: Non Disclosure Agreement 
NETTO: New Test Tool (Nokia internal, see the following section) 
NTP: Normal temperature and pressure (see laboratory environment in the following 
section) 


 
Verification Methods Of 
Materials 
 
5 (90) 
DQD/TQ, Device R&D 
 
 
 
 
17.12.2009 
Confidential 1H2010 release 
 
 
SCE: Specular component excluded 
SCI: Specular component included 
SEM: Scanning Electronic Microscope 
SFS: Finnish Standards Association 
SPR: Standard Product Requirements (Nokia internal) 
STR: Standard Technology Requirements (Nokia internal) 
UV: Ultraviolet 
1.3 Definitions 
Measurement: A procedure to obtain the values of certain properties of a sample 
focusing on the sample status / conditions but not contain any procedure which tends to 
change the conditions / properties of samples (the instances: dimensions, optical 
measurements / electric measurements, visual inspection and etc.) 
Test: A procedure to examine or accelerate the condition change of a sample, by one 
or more external factors (the instances: temperature cycling, humidity cycling, corrosion, 
wearing and etc.) 
Test duration: The time used by a specific test procedure. It is hour-based. If day or 
week is used, it shall be calculated as follows: 
 
One day = 24 hours 
 
One week = 7 days = 168 hours 
Laboratory environment: The environment meets the following requirements: 
 
Temperature = + 20 °C ~ 25 °C 
 
Humidity = 40% ~ 60%RH 
Sample: A mechanical unit or element manufactured or processed consisting of one 
or more materials. It may have specific structures associated with certain functionalities 
or be just one piece of raw material 
 
Coated sample: A sample that has a substrate and one or more layers adhered 
to the surface using a factory process. Unless redefined in each section, 
substrates generally include  
o Polymer, metal, and glass 
The coating generally includes 
o Metallization, painting, printing, and laminated film 
 
Uncoated sample: A sample in which substrate includes all engineering materials 
listed against the coated sample 


 
Verification Methods Of 
Materials 
 
6 (90) 
DQD/TQ, Device R&D 
 
 
 
 
17.12.2009 
Confidential 1H2010 release 
 
 
NETTO: a tool developed to simulate application environments. It is recommended to 
use it for all tests which require phone mechanics. Practical phone mechanics is 
preferred when it is available.                                                                                                             


 
Verification Methods Of 
Materials 
 
7 (90) 
DQD/TQ, Device R&D 
 
 
 
 
17.12.2009 
Confidential 1H2010 release 
 
 
 
2. MEASUREMENTS 
2.1 Visual  
2.1.1 Visual inspection 
REFERENCES 
 
MOSS 800/1 Control of Visual Quality 
 
MOSS 800/2 Painted Parts 
MOSS 800/3 Plated Parts 
 
MOSS 800/6 Plastic and Rubber Parts 
MOSS 800/7 Printings 
 
MOSS 800/11 Metal Parts 
DEFINITION AND REQUIREMENTS 
This section defines the method and procedure for visual inspection. 
This method is used to examine the defects of samples visually. 
This measurement applies to all types of samples, the coated and the uncoated, the 
tested or the untested. 
All the visual defects defined in project/product specifications (or other related 
documents) shall be considered. 
If no definitions in the related documents, the following defects shall be examined when 
applicable: 
 
Contaminations and corrosion products 
 
Scratching and cracking 
 
Blistering and peeling 
 
Wearing 
 
Color change 
The defects observed shall be recorded and scored by comparing with the corresponded 
graphic gauge provided in Appendix of this document. 
For recording the defects, an optical microscope can be used and the recording of 
images can be conducted outside of the assessment cabin. 
Samples used in this measurement may come either directly from manufacturing 
processes or have been the subject to other tests. 
Samples used in this measurement shall be kept in their original conditions with no wet 
cleaning processes used prior to the measurement unless required in project / product 
specifications or other related documents. 


 
Verification Methods Of 
Materials 
 
8 (90) 
DQD/TQ, Device R&D 
 
 
 
 
17.12.2009 
Confidential 1H2010 release 
 
 
A clean source of compressed air may be used to remove dust from the environment. 
All measurements shall be conducted in a clean laboratory environment. 
Amount of sample: optional (application dependent) 
SETUP 
Standard assessment cabin and optical microscope 
The assessment cabin shall have equipped with D65 and UV light source. 
The microscope shall be stereo optical microscope with the capability for a magnification 
up to 200 
The measurement device shall be installed in the laboratory environment. 
The measurement devices shall be calibrated and maintained in the normal working 
condition 
 
 
Figure 1: Illustration of an assessment cabin 
 
PROCEDURE 
 
Select the light source (D65 or UV) according to project / product specifications 
(requirements). If not defined in specifications (requirements), use the following 
instructions 
o For untested samples, UV to be selected if samples contain fluorescent 
material and D65 to be selected for others 
o For tested samples, both D65 and UV are required 
 
Keep the observing distance between eyes and sample to be ~ 30 cm 
 
Examine the sample for the defects listed in the requirements 
o Any defects shall be recorded by an optical microscope and scored by 
comparison with the corresponded graphic gauge (see Appendix) 


 
Verification Methods Of 
Materials 
 
9 (90) 
DQD/TQ, Device R&D 
 
 
 
 
17.12.2009 
Confidential 1H2010 release 
 
 
o The recording can be conducted outside of the assessment cabin, with a 
proper magnification 
The images shall be recorded with the text notes, describing the conditions of the 
sample and the images (such as magnification or size bar and etc). 
ACCEPTANCE CRITERIA 
 Referring to project / product specification or other related documents (e.g. material 
STR). 
 
2.2 Mechanical  
2.2.1 Residual Stress 
REFERENCE 
 
SPR_a – Product Reliability, DOORS Production DB/SPR/Global SPR 
DEFINITION AND REQUIREMENTS 
This section defines the method and procedure for residual stress measurement. 
This method is used for the uncoated transparent samples manufactured of either optical 
plastic or glass. The residual stress can then be observed when it is veiwed under a 
polarized light source.  The presence of stress concentrations will change the 
polarization properties of the transmitted light. 
The samples to be used in this measurement must have a transmittance equal or larger 
than 90%.  
For other type of material samples, this method is not applicable. 
The samples to be used in this measurement shall be directly from manufacturing 
processes, or have been subjected to other tests. 
The samples to be used in this measurement shall have a clean surface. If needed, DI 
water cleaning process can be applied. 
Cleaning process shall be conducted in laboratory environment and must under no 
circumstance be done using either chemicals or high temperatures, since these may 
change the conditions of residual stress inside of sample. 
The measurements shall be conducted in the laboratory environment. 
Minimum amount of samples: 3 (for each cavity) 
SETUP 
Standard polariscope (strain viewer) or compatible measurement devices 
The measurement devices must have a laboratory light source, preferably with both 
monochromatic and full wavelength light sources 


 
Verification Methods Of 
Materials 
 
10 (90) 
DQD/TQ, Device R&D 
 
 
 
 
17.12.2009 
Confidential 1H2010 release 
 
 
The measurement devices shall have equipped with a recording system so that the 
images of measurements can be recorded. 
The measurement devices shall be installed in the laboratory environment. 
The measurement devices shall be calibrated and maintained in the normal working 
condition 
 
Figure 2 
Illustration of a Strain viewer 
 
PROCEDURE 
1. Turn light source ON 
2. Put sample on sample plate 
3. Inspect sample and evaluate the level or place of stresses. 
4. The color of residual stresses is different depending on used light or type of 
tested material. 
The results shall be recorded in the format of images with proper text notes, to explain 
the location and level of stresses. 
 
 
Figure 3  
Illustration of results, typical critical areas around injection point 
 
