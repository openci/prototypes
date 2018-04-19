# Introduction

This prototype aims to demonstrate how CI/CD Systems developed, maintained
and operated across different open source communities can be enabled to
communicate with each other with event broadcasting.

This prototype **does not** propose a messaging protocol but instead tries to
highlight some of the key areas which might help us to start conversations
around what is needed to initiate the work to look into possibilities to switch
to event driven CI/CD from the traditional timer/polling based CI/CD, helping us
to establish federation of CI/CD Systems.

# Key Considerations and Constraints

Some key considerations and constraints that are taken into account by the prototype
are detailed below.

## Complex/E2E CI/CD Flows

Majority of open source projects work pretty near to SCM and do not go far from where
the development happens. This results in difficulty when it comes to E2E Integration
and Testing since the CI/CD Systems are not built for this type of scenarios.

Recently communities started to think about and work on system level integration and
testing. This naturally requires evolution of the CI/CD Systems developed and used by
these communities and within open source ecosystem in general to support CI/CD flows
that span across multiple communities and pass through multiple community boundaries.

It is important for open source communities to work on these challenges together in
order to establish common understanding and methodology so the efforts to bring up
complex CI/CD Flows is reduced.

## Loose Coupling

Messaging makes applications loosely coupled by communicating asynchronously, which
also makes the communication more reliable because the two applications do not have
to be running at the same time. Messaging makes the messaging system responsible
for transferring data from one application to another, so that applications can focus
on what data they need to share as opposed to how to share it. [1]

## Event Broadcasting

In software architecture, publish-subscribe is a messaging pattern where senders of
messages do not program the messages to be sent directly to specific receivers but
instead categorize published messages into classes without knowledge of which subscribers,
if any, there may be. Similarly, subscribers express interest in one or more classes
and only receive messages that are of interest, without knowledge of which publishers,
if any, there are. [2]

## Being Agnostic to the Technology and Processes

Communities use various SCM Systems (Gerrit, Gitlab, Github), CI Tooling (Jenkins,
Zuul, Gitlab CI) and Artifact Repositories (Nexus, Google Cloud Storage).

This prototype aims to demostrate the importance of being agnostic to the underlying
technologies used by the community CI/CD Systems. As long as these systems
adhere to the **yet to be defined** messaging protocol, the underlying technology used
by them is not a concern in event driven CI/CD since it is up to the communities to 
use the tooling they have in a way that benefits them most.

The only requirement from the tooling perspective is that the tools used by the
communities are able to publish and consume events.

Apart from the tooling used to construct the CI pipelines, the processes between
communities differ. It is important for CI/CD Systems to be agnostic to the processes
followed by the communities as well in order to achieve event driven end-to-end
integration flows.

In the end, the machines communicate via events that conform to the protocol and take
appropriate actions.

## Scalability

It is important to keep the scalability aspects in mind as well and treat the CI/CD
Systems as decentralized systems.

This can be achieved by the event broadcasting, enabling the distribution and management
of CI activities in a scalable manner and removing the bottlenecks that might be introduced
by the use of CI tooling and/or the processes and the way of working followed by the communities
that are not capable of providing decentralization out of the box.

Scalability in this case mean both horizontal and vertical which enables the use of event driven
CI/CD in a single community context or cross community context.

## Flexibility

As mentioned above,it is important to stress the importance of consumers not
being aware of other entities who might be interested in what is developed by originating
communities. There could be 0..n number of consumers out there but the only requirement
on the communities who publish information is to adhere to the messaging protocol and
make the information and artifacts that could be consumed by the interested communities
publicly accessible.

Apart from the number of consumers, the consumers may be interested in subset of
activities that are happening in other CI/CD flows so they can subscribe to the events
published upon the completion of those certain activities. Again, this is not
something that requires the knowledge on publishers' side.

As highlighted above, the main responsibility is on the consumers since apart from
adhering the same messaging protocol, they will need to use the information provided
by the originating communities in order to extract the metadata to retrieve the artifacts
with the desired confidence/quality level from their origin and any other information
they may require.

In summary, the community CI Systems do not tell each other what to do via hooks or
RPCs but instead they tell what happened and the necessary actions are taken by the
consumers. (prescriptive vs descriptive) This gives great flexibility to construct
CI Pipelines that span across multiple communities.

## Other Considerations and Concerns

On top of what is listed above, there are other considerations the event driven CI/CD Systems
need to take into account such as

* traceability
* reproducibility
* high availability
* performance
* security

Since this prototype is limited in its scope, the details of these topics are not covered
here.

# The Proposal

As highlighted in the previous chapter, event driven architecture provides 
solutions for (some of) the challenges we as open source communities face in 
CI/CD. By using event broadcasting and federated approach, CI/CD Systems
developed, operated, and used by the communities can address the challenges they
may be facing when it comes E2E Integration and Testing and with the CI/CD Flows
that span across multiple communities.

The proposal is to
* develop and standardize a messaging protocol in an open and collaborative 
manner
* introduce the federation concept so the community CI/CD Systems can and will 
be able to continue to be developed and operated in same fashion and
independently
* ensure the community CI/CD Systems adhere to the messaging protocol
* implement/enable what the messaging protocol and federation require on
community CI/CD Systems


# The Scenario

Open Platform for NFV (OPNFV) facilitates the development and evolution of NFV
components across various open source ecosystems. [3]

OpenDaylight (ODL) is a modular open platform for customizing and automating
networks of any size and scale. [4]

As part of the system level integration and testing efforts of OPNFV, different
compositions of the reference platform (scenarios) are created. One of these
scenarios is OpenStack with ODL. Very high level CI Flow which starts from a change
in ODL Gerrit and goes till the OPNFV system level testing can be seen on the diagram
below.

<diagram>

The prototype will use a very limited cross community CI Flow to demostrate event 
driven CI/CD and Federation. The 3 main activities that happen in this limited flow are

* artifact creation
* baseline generation
* confidence level

As part of the prototype, a simple promotion mechanism will also be demonstrated.

<diagram>

## Activities to be Demonstrated

### Artifact Creation: ODL CI

ODL RelEng/Autorelease project builds every ODL project from source for every
active branch, including master using the corresponding Jenkins jobs. Each of
those jobs, when the build is successful, produces build artifacts that include
an OpenDaylight distribution. [5] As explained on the documentation, it is
not straightforward to find and fetch these artifacts programmatically by the
users, for example OPNFV CI.

In Event Driven CI, the ODL RelEng/Autorelease project Jenkins jobs can publish
events upon the successful completion of the builds and whoever is interested in
those events can subscribe to them and get the information out of the events,
locating the latest and greates version of the ODL Distribution for the branch
they may be interested in.

### Baseline Generation: OPNFV CI

OPNFV needs to ensure the latest ODL Distribution built and made available by ODL
RelEng/Autorelease project works fine before they are taken into the main OPNFV
CI Flow. In order to achieve that, a simple mechanism to generate candidate
baseline which consists of latest verified version of the OpenStack and
the latest ODL Distribution that has been made available by ODL RelEng/Autorelease.

This can be achieved by subscribing artifact created events published by ODL
RelEng/Autorelease for the branch OPNFV is interested in, extracting the metadata
such as artifact version, location, etc. and generating/publishing a new event
that contains the baseline to be tested which consists of the metadata of verified
version of OpenStack and latest ODL distribution.

It is important to mention here is that the baseline can consists of artifacts,
other baselines and artifacts and baselines depending on use case.

### Confidence Level: OPNFV CI

The jobs in OPNFV CI can subscribe to baseline generated event published by
OPNFV CI itself this time. By doing this, the jobs on OPNFV CI that are interested
in new baseline get triggered, deploying and testing the composed platform using
the verified version of OpenStack and the latest version of ODL Distribution.

Upon completion of the jobs, a new event stating the new confidence level the
baseline gained can be published. Confidence level in this context is a quality
stamp that is applied to candidate baseline upon successful completion of the
corresponding activity in CI. As well as baselines, standalone artifacts could
gain (multiple) confidence levels while they traverse through different stages within
CI Flow which may well be distributed across different communities, passing through
multiple community boundaries.

In this prototype, the confidence level that gets applied to the latest ODL Distribution
built by ODL RelEng/Autorelease means that this version of ODL is good to use for
the next stages within OPNFV CI. If desired, ODL CI can also subscribe to this event
and apply a quality stamp on their side stating that the corresponding version of the
ODL Distribution successfully passed OPNFV testing and other users can get this version
with relatively higher confidence.

## Event Types and the Metadata to Use for the Prototype

In order to bring up this prototype and have something realistic enough, 3 different event types
to be used during this work are defined. These event types are

* ArtifactCreated
* BaselineDefined
* ConfidenceLevelModified

Apart from the event types, certain key/value pairs need to be included in all events such as

* eventId: unique ID of the event ("EVENT_ID": "D10EFFE9-2BC0-4C58-AC38-3D331A195C47")
* eventTime: The time which the event was generated to be published ("EVENT_TIME": "12:34:56UTC")
* buildUrl: The url to build which this event is published by ("BUILD_URL": "https://url/to/build/#")

In addition to common key/value pairs, The events have additional metadata depending on their types
as can be seen below.

**ArtifactCreated event**

* artifactUrl: The url pointing to the location on artifact repository ("ARTIFACT_URL": "https://url/to/artifact")
* projectBranch: The branch the artifact is built for. ("PROJECT_BRANCH": "master")
* confidenceLevel: The confidence level (quality stamp) the artifact gained ("AUTORELEASE": "SUCCESS") The value can be Jenkins build result.

**BaselineDefined event**

* baselineName: The name of the baseline that's defined. ("BASELINE_NAME": "os-odl-nofeature")
* baselineUrl: The prototype will keep the baseline information in text files and this url points to that location ("BASELINE_URL": "https://url/to/baseline")
* consistsOf: What this baseline contains ("CONSIST_OF": "opendaylight-master-1.2.3,openstack-master-17.18.19")

**ConfidenceLevelModified event**

* baselineName: The name of the baseline that's defined. ("BASELINE_NAME": "os-odl-nofeature")
* baselineUrl: The prototype will keep the baseline information in text files and this url points to that location ("BASELINE_URL": "https://url/to/baseline")
* confidenceLevel: The confidence level (quality stamp) the baseline gained ("OPNFV_ACCEPTANCE": "SUCCESS") The value can be Jenkins build result.

Example events can be seen in OpenCI Gitlab Repo. [6]

## Tooling to be used by the Prototype

The prototype will use openly available/already existing tooling to demonstrate the ideas.

OPNFV and ODL projects are hosted by Linux Foundation and the projects use Jenkins as part
of their CI/CD Systems so the prototype will also use Jenkins as CI Engine component.

Jenkins community developed *JMS Messaging Plugin* [7] which triggers builds
using messages published towards topics/queues on message brokers. Apart from consuming
messages, it can also publish messages as well.

The 2 message brokers supported by JMS Messaging Plugin are ActiveMQ and FedMsg.
ActiveMQ is chosen to be used due to difficulty bringing up FedMsg during the preparation
of this document. [8]

Fetching artifacts will be done using Nexus REST API within a bash script. [9]

An important thing to highlight here is that the tooling selected for the prototyping work
does not mean this is the tooling proposed to be used. They are chosen to get things off the
ground and demonstrate the ideas. The important thing to focus on this prototype is to see
if the event driven CI/CD help us address some of the challenges we are facing. If the
community forms a consensus around what this prototype demonstrates, further actions can and
will be taken to clarify the tooling to use by taking other CI Engines such as Zuul into
consideration.

## Prototype Phases

Prototype will be developed in 2 phases.

* Hello World: This phase aims to establish communication between ODL and OPNFV CI/CD Systems
on sandbox Jenkins instances.
* Real Deal: This phase aims to move the pieces developed during the previous phase to
production Jenkins instances and attempt to fetch the artifacts, generate baselines, run
testing and publish confidence level events.

Please see the backlog on Gitlab. [10]
The community is encouraged to involve in developing the prototype in order to bring even
more ideas and try them out for real. The community will be kept up to date regarding the
progress with the prototype and everything will be available publicly.

# Conclusions

As stated throughout this document, this prototype aims to demonstrate the challenges in
E2E Integration and Testing we as open source communities face and start the conversation
around evolving CI/CD Systems our communities use to support event driven CI/CD and CI/CD
Federation.

The impacts of this on community CI/CD Systems are pretty limited but result in benefits for
the wider ecosystem. The ideas represented here could enable us to continue establishing common vocabulary
within open source ecosystem supported by a messaging protocol, resulting in
creation of a layer across open source communities which acts like a glue between CI/CD Systems.

# References

[1] https://www.amazon.com/o/asin/0321200683/ref=nosim/enterpriseint-20  
[2] https://en.wikipedia.org/wiki/Publish%E2%80%93subscribe_pattern  
[3] https://www.opnfv.org/  
[4] https://www.opendaylight.org/  
[5] http://docs.opendaylight.org/projects/integration-packaging/en/latest/autorelease-builds.html  
[6] https://gitlab.openci.io/openci/prototypes/tree/master/federated-cicd/examples  
[7] https://plugins.jenkins.io/jms-messaging  
[8] http://activemq.apache.org/  
[9] https://blog.sonatype.com/2011/01/downloading-artifacts-from-nexus-with-bash/  
[10] https://gitlab.openci.io/openci/prototypes/issues  
