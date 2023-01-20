# MELT Library:

This MELT library is intended to provide a simplified interface for a variety or metric, event, logs and trace software.
The idea is that each service you might use to capture this within your application (Think logs, apm, etc) would be an emitter.

These emitters have their own, baked in configuration needs. However, a client would be allowed to keep most of their code from changing, if those endpoints change.
An example use case is that software is created with a tight coupling to 'Service A' and then after a few years, 'Service B' appears. This means, potentially, a lot of
updates to the code to account for this.


The MELT Library in this case, would be the only portion coupled into the main software. A new emitter could be added into the service without the tight coupling.
This would allow updates for backend changes to metrics, events, logs and traces to be made in isolation, tested and deployed more quickly.

There is also an opportunity to allow the type and depth of the logs or traces needed in real time, once the actual service is running. This could permit debugging to
take place by specifying a specific tracing class only after some breakpoint in the code. This could allow for debugging problems which are only found after running in production.


## High Level Design:

The intention of this is to simplify everything down only to what is needed. There is a light version of Hex Architecture taking place here.
The core domain code should change the least frequently and house the various interfaces.

The Adaptors are for new ways in which this code needs to be accessed (Say, FastAPI needs something differnt than a CLI Application for some reason) or a different configuration source.

The Ports are generally, the emitters themselves. These are services which handle a specific job but are conforming to a specific set of signatures.

These are handled through a light version of dependency injection at the 'Main' level, where everything should be ultiately composed and instantiated.


## Example:
In progress.


## Notes and Discussion:
  1. 

## References:
  1. 