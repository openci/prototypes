Introduction
============

This prototype aims to demonstrate how CI/CD Systems developed, maintained
and operated across different open source communities can be enabled to
communicate with each other with the use of a messaging protocol.

This prototype **does not** propose a messaging protocol but instead tries to
highlight some of the key topics which might help us to start conversation
around what is needed to initiate the work to establish federation of CI/CD
Systems.

Key Considerations and Constraints
==================================

Few key considerations and constraints that are taken into account by the prototype
have been described below.

Being Agnostic to the Technology
--------------------------------

Communities use various SCM Systems (Gerrit, Gitlab, Github), CI Tooling (Jenkins,
Zuul, Gitlab CI) and Artifact Repositories (Nexus, Google Cloud Storage).

This prototype aims to demostrate the importance of being agnostic to the underlying
technologies used by the communities. As long as the community CI Systems
adhere to the messaging protocol, the underlying technology used by them is not a
concern in federated CI/CD since it is up to the communities to use the tooling they
have in a way that benefits them most.

The only requirement from the tooling perspective is that the tools used by the
communities are able to publish and consume events.

In the end, the machines communicate via the protocol and they take actions humans
tell them to do.

Traceability
------------

TBD

Scalability
-----------

It is important to keep the scalability aspects in mind as well and treat the CI/CD
Systems as decentralized systems.

This can be achieved by the event broadcasting, enabling the distribution and management of CI activities
in a scalable manner and removing the bottlenecks that might be introduced by the use of
CI tooling that is not capable of providing decentralization out of the box.

Flexibility
-----------

Aside from what this prototype aims to demonstrate, it is important to state
that the communities who develop certain technologies are not expected to know
about other entities who might be interested in what is developed by originating
communities. There could be 0..n number of consumers out there but the only requirement
on the communities who publish information is to adhere to the messaging protocol and
make the artifacts that could be consumed by the interested communities publicly
accessible.

Apart from the number of consumers, the consumers may be interested in subset of
activities that are happening in upstream so they can subscribe to the events
published upon the completion of those certain activities. Again, this is not
something that requires the knowledge on publishers' side.

As highlighted above, the main responsibility is on the consumers since apart from
adhering the same protocol, they will need to use the information provided by the
originating communities in order to extract the metadata to retrieve the artifacts
with the desired confidence/quality level from their origin.

In summary, the community CI Systems do not tell each other what to do but instead
they tell what happened on their side and the necesseary actions are taken by the
consumers. (prescriptive vs descriptive)


The Scenario
============

Open Platform for NFV (OPNFV) facilitates the development and evolution of NFV
components across various open source ecosystems. [1]

OpenDaylight (ODL) is a modular open platform for customizing and automating
networks of any size and scale. [2]

As part of the system level integration and testing efforts of OPNFV, different
compositions of the reference platform (scenarios) are created. One of these
scenarios is OpenStack with ODL.

The prototype will use a very limited CI Flow to demostrate event driven CI/CD
and CI/CD Federation. The 3 main activities that happen in this flow are

* artifact creation
* baseline generation
* confidence level

As part of the prototype, a simple promotion mechanism will also be demonstrated.

<diagram>

Artifact Creation: ODL CI
-------------------------

ODL RelEng/Autorelease project builds every ODL project from source for every
active branch, including master using the corresponding Jenkins jobs. Each of
those jobs, when the build is successful, produces build artifacts that include
an OpenDaylight distribution. [3] As explained on the documentation, it is
not straightforward to find and fetch these artifacts programmatically by the
users, for example OPNFV CI.

In Event Driven CI, the ODL RelEng/Autorelease project Jenkins jobs can publish
events upon the successful completion of the builds and whoever is interested in
those events can subscribe to them and get the information out of the events.

Baseline Generation: OPNFV CI
-----------------------------

OPNFV needs to ensure the ODL Distribution built and made available by ODL
RelEng/Autorelease project works fine before they are taken into the main OPNFV
CI Flow. In order to achieve that, a simple mechanism to generate candidate
baseline which consists of latest verified version of the OpenStack and
the latest ODL Distribution that has been made available by ODL RelEng/Autorelease.

This can be achieved by subscribing artifact creation events published by ODL
RelEng/Autorelease for the branch OPNFV is interested in, extracting the metadata
such as artifact version, location, etc. and generating/publishing a new event
that contains the metadata of verified version of OpenStack and latest ODL
distribution.

Confidence Level: OPNFV CI
--------------------------

The jobs in OPNFV CI can subscribe to baseline generation event published by
OPNFV CI itself this time. By doing this, the jobs on OPNFV CI that are interested
in new baseline get triggered, deploying and testing the composed platform using
the verified version of OpenStack and the latest version of ODL Distribution.

Upon completion of the jobs, a new event stating the new confidence level the
baseline gained can be published. Confidence level in this context is a quality
stamp that is applied to artifacts or baselines upon successful completion of the
corresponding activity in CI. Artifacts and baselines could gain multiple confidence
levels while they pass through different stages within CI.

In this prototype, the confidence level that gets applied to the latest ODL Distribution
built by ODL RelEng/Autorelease means that this version of ODL is good to use for
the next stages within OPNFV CI. If desired, ODL CI can also subscribe to this event
and apply a quality stamp on their side stating that the corresponding version of the ODL Distribution
successfully passed OPNFV acceptance testing and other users can get this version
with relatively higher confidence.

References
==========

[1] https://www.opnfv.org/
[2] https://www.opendaylight.org/
[3] http://docs.opendaylight.org/en/stable-oxygen/submodules/integration/packaging/docs/autorelease-builds.html

