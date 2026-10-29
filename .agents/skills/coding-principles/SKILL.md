---
name: coding-principles
description: Fundamental principles for code clarity, naming uniformity, live execution, and clean architecture.
---
Coding principles.
Code is the way to communicate with the machine, it is critical that it be clear to a person who enters from the outside.
The architecture, structure and names of the objects in the code must tell in the clearest way what is happening in the code. It must be that way.
Updating code - it is sensitive, it must be done gently, not to refactor what you were not asked to do.
3 \ 4 lines must be added at the beginning of the file that explain how this file fits into all the existing code.
Building code requires checking that it actually connects and works.
Code should be elegant, cleverness, tricks, sophisticated things should not be in the code, they should only be in certain cases.
Uniformity of concepts and names - the choice of names is very important. If a component in the system has a name, that same name must be preserved every time it is mentioned, everywhere it appears. One concept, one name. This is what makes code easy to understand for someone reading it from the outside.
For example, if a service has tests and dedicated auxiliary functions that support those tests, the same name should run through all of them - the service, its tests, and its helpers - so the reader quickly understands what the auxiliary functions serve. Do not invent a new synonym for something that already has a name; reusing the established name is clarity, inventing variants is confusion.
The way of working is - building something, once it is assembled - you make sure that it actually works and continue.
This is a research and development project: keep the code clean without dead legacy shims, while strictly preserving the shared experiment language (concepts, names, tool signatures, and structure) across experiments so that anyone moving from one experiment to the next immediately understands it and previous experiments remain comparable.
We will always strive for there to be only one clear and direct way to use the code. We will only deviate from this when necessary.
Observability and Ground Truth Execution: Never substitute real logic or live execution with hardcoded mock data in notebooks, exploration scripts, or evaluation workflows. Every data transformation must run through the real code path so that changes to models, prompts, parameters, or algorithms immediately produce observable results.
Integration & Live Guard Verification: Prioritize testing via live CLI commands, end-to-end integration checks, and the repository's `guard_cmd` regression suite (`uv run ...`) over isolated, trivial mock unit tests.