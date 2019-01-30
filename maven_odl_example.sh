# mvn archetype:generate \
	# # -DarchetypeGroupId=org.opendaylight.archetypes \
	# -DarchetypeGroupId=org.opendaylight.controller \
	# -DarchetypeArtifactId=maven-archetype-quickstart \
    	# -DinteractiveMode=false \
	# -DarchetypeVersion=1.7.0-SNAPSHOT \
     	# -Dversion=0.7.2
# SVERSION="opendaylight.snapshot"
SVERSION="opendaylight.release"
# AVERSION="1.4.0-SNAPSHOT"
# AVERSION="1.2.0-Boron" # worked
AVERSION="1.2.0-Boron"
PNAME="odl_p1"
mvn archetype:generate \
	-DarchetypeGroupId=org.opendaylight.controller \
        -DarchetypeArtifactId=opendaylight-startup-archetype \
	-DarchetypeRepository=http://nexus.opendaylight.org/content/repositories/$SVERSION/ \
	-DarchetypeCatalog=remote \
	-DarchetypeVersion=$AVERSION \
     	-DgroupId=org.opendaylight.$PNAME \
     	-DartifactId=$PNAME \
	-DclassPrefix=TEST \
	-Dcopyright=bh2019 \
 	-DinteractiveMode=false
	# -Dpackage=org.opendaylight.$PNAME \ 
