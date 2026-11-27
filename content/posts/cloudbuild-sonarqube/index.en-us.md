+++
title = "GCP - Integrating SonarQube with Cloud Build"
slug = "cloudbuild-sonarqube"
date = 2026-04-10T00:00:00-04:00
summary = "On GCP, adding the SonarQube code review tool to Cloud Build, the CI/CD service, keeps as much bad code out as possible, so your applications are more secure and of higher quality."
translation = { model = "claude-opus-5-5", sourceHash = "9334e2aa47e3" }
+++

{{< archive-note year="2023" >}}

Code security and code quality matter a lot in any codebase. In commercial projects especially, they largely decide whether a project succeeds. When security and quality are poor, bad code can cause serious outages in production. The results can be disastrous, with direct financial losses for the company and a loss of trust in the team.

On GCP, you can integrate the SonarQube code review tool with Cloud Build, the CI/CD service, to keep as much bad code out as possible. That way your applications run in a more secure, higher-quality state.

This post shows how to integrate SonarQube with Cloud Build so you can safely deploy new containers to k8s.

## The tools

### [Cloud Build](https://cloud.google.com/build)

I covered GCP Cloud Build in an earlier post - if you haven't read it yet, you can find it [here]({{< relref "/posts/cloudbuild-probe" >}}).

### [SonarQube](https://www.sonarsource.com/products/sonarqube/)

SonarQube is an open-source code analysis and review tool built by SonarSource and first released in 2006. As of March 2023, the latest stable version is 9.9, released that February.

SonarQube's main job is to continuously analyze and assess the quality of a project's source code. It finds wasteful code, such as duplicated code, and problems in the codebase, such as errors, potential security vulnerabilities and potential bugs. It shows all of this, along with other useful information about the code, in the SonarQube UI.

Through plugins, SonarQube supports code quality checks for 19 programming languages, including Java, C#, JavaScript, TypeScript, Python and PHP.

SonarQube scans and analyzes the code developers write against predefined quality and security rules, then presents the results visually from several angles. That makes it easier for developers to clean up old code and write to a consistent standard.

---

## SonarQube - Quality Gate

A Quality Gate is exactly what the name says: the gate your code has to pass in a SonarQube review. SonarQube compares the overall quality of new code against the gate you've defined to decide whether the new code meets the bar.

In a Quality Gate, you can set standards for different metrics:

- Coverage - test coverage
- Duplicated Lines (%) - percentage of duplicated code
- Maintainability Rating - how easy the code is to maintain
- Reliability Rating - how reliable the code is
- Security Hotspots Reviewed - percentage of security hotspots that have been reviewed
- Security Rating - how secure the code is

You can also set conditions on issues across the whole codebase:

- Blocker Issues - the most severe code issues
- Critical Issues - high-severity code issues

Each metric can have a threshold, for example:

- Coverage > 90%
- Duplicated Lines < 5%
- Maintainability Rating > B
- Reliability Rating >= B
- Security Hotspots Reviewed = 100%
- Security Rating = A
- Blocker Issues <= 2
- Critical Issues < 5

If any metric fails, the Quality Gate returns a Failed status.

Quality Gates offer other metrics too. If you're curious, see the [metric definitions](https://docs.sonarsource.com/sonarqube-server/9.8/user-guide/metric-definitions).

### Integrating SonarQube with Cloud Build

```text
  - name: someBaseImage
    id: Run SonarQube to Analyze New Container Codebase
    entrypoint: 'bash'
    args:
      - -c
      - |
        ./gradlew sonarqube -Dsonar.qualitygate.wait=true \
        -Dsonar.login=loginHashValue --no-daemon

    allowFailure: false
```

Here we define a step in the Cloud Build pipeline named:
"Run SonarQube to Analyze New Container Codebase"

In this step, Cloud Build runs SonarQube, logging in with the token in `-Dsonar.login=loginHashValue`, then compares the scan results for the current code with the SonarQube Quality Gate you defined.

- If the Quality Gate passes, the step returns `SUCCESS`
- If the Quality Gate fails, the step returns `FAILURE`

With Gradle, we need to add `--no-daemon` so the SonarQube process runs properly.

The `-Dsonar.qualitygate.wait=true` flag makes Cloud Build wait for SonarQube's Quality Gate result before it continues.

If the current code doesn't pass the Quality Gate, Cloud Build uses the `allowFailure` setting to decide whether to move on to the next step.

Here we set `allowFailure: false`, which means this step isn't allowed to fail. As soon as it fails, Cloud Build stops the run and returns a final result of `FAILURE`.

`allowFailure` already defaults to `false`, so leaving it out has the same effect. If you set it to `true`, Cloud Build keeps running the remaining steps when this one fails, and the build still returns `SUCCESS` as long as all the other steps succeed.

---

## Summary

Every business runs on software, and software is written by engineers, so code quality and security problems are bound to come up. A project team should think about likely code issues from the very start and pick the right tools to deal with them. SonarQube is an easy choice. When you deploy to k8s on GCP, building SonarQube into a CI/CD service such as Cloud Build is a sound process, and with the right tools you can go a long way toward keeping your software running safely and correctly.

Finally, if this article has been helpful to you, I'd love to hear your thoughts. Let's connect, share our experiences, and continue learning together.
