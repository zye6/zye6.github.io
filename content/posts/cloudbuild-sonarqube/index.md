+++
title = "GCP - Cloud Build集成SonarQube"
slug = "cloudbuild-sonarqube"
date = 2026-04-10T00:00:00-04:00
summary = "在GCP中, 通过使用CI/CD服务 Cloud Build 集成 SonarQube 代码审查工具, 可以最大程度地限制坏代码的存在, 从而让应用程序以更安全和更高质量的状态运行."
readingTime = 1
+++

{{< archive-note year="2023" >}}

代码安全和代码质量在代码库里有着非常重要的地位, 尤其是在商业项目中, 这两项指标基本决定了项目的成功与否. 当代码安全和代码质量令人堪忧时, 这些坏代码可能会在生产环境中引发严重的故障, 从而导致灾难性的后果, 并会直接造成企业的经济损失和团队的信任危机.

在GCP中, 通过使用CI/CD服务Cloud Build, 集成SonarQube代码审查工具, 可以最大程度的限制坏代码的存在, 从而使应用程序以较安全和高质量的状态运行.

此篇博客将介绍如何将Cloud Build集成SonarQube, 从而安全的部署新容器到k8s平台上.

## 工具介绍

### [Cloud Build](https://cloud.google.com/build)

关于GCP Cloud Build, 我已经在之前的博客中介绍过了 - 还没有阅读的读者, 可以点[这里](/2026/cloudbuild-probe/)进行阅读.

### [SonarQube](https://www.sonarsource.com/products/sonarqube/)

SonarQube是由SonarQube团队开发的开源代码分析审查工具, 发布于2006, 截至3月, 目前稳定的版本为2023年2月发布的9.9版本.

SonarQube最大的用途, 就是可以持续的分析和评估项目源代码的质量, 通过SonarQube可以检测出项目中的废代码, 例如重复代码; 亦或者代码库中的错误, 潜在安全漏洞, 潜在bug, 等其他有用的代码信息, 并通过SonarQube UI一一展现出来.

SonarQube通过插件方式, 可以支持包括Java, C#, JavaScript, TypeScript, Python, PHP 等19种编程语言的代码质量管理与检测.

SonarQube通过定义好的代码质量和安全规则, 对开发人员编写的代码进行扫描和分析, 并将分析结果用多角度, 多维度, 可视化的方式呈现出来, 以方便开发人员进行旧代码的优化和规范编写.

---

## SonarQube - Quality Gate:

Quality Gate, 正如名字所表达的意思, 这是SonarQube代码审查的质量门. SonarQube会对比参照新代码的整体质量与已经定义好的质量门, 来判断新代码是否符合要求.

你可以在质量门里定义不同的代码标准:

- Coverage - 测试覆盖率
- Duplicated Lines (%) - 重复代码百分比
- Maintainability Rating - 代码维护难易度评分
- Reliability Rating - 代码可读性评分
- Security Hotspots Reviewed - 代码安全问题
- Security Rating - 代码安全评分

同时也可定义总代码的质量问题:

- Blocker Issues - 最高级别代码问题
- Critical Issues - 高级别代码问题

每一项指标都可以设置阈值, 如:

- Coverage > 90%
- Duplicated Lines < 5%
- Maintainability Rating > B
- Reliability Rating >= B
- Security Hotspots Reviewed <= C
- Security Rating = A
- Blocker Issues <= 2
- Critical Issues < 5

当任何一项代码指标不通过时, 质量门会返回Failed状态.

质量门还提供其他的代码指标, 感兴趣的读者可以点[这里](https://docs.sonarqube.org/9.8/user-guide/metric-definitions/)进行了解.

### Cloud Build集成SonarQube

```text
  - name: someBaseImage:
    id: Run SonarQube to Analyze New Container Codebase
    entrypoint: 'bash'
    args:
      - -c
      - |
        ./gradlew sonarqube -Dsonar.qualitygate.wait=true \
        -Dsonar.login=loginHashValue --no-daemon

    allow_failure: false
```

在这里, 我们在Cloud Build Pipeline里面定义了一步名为:
"Run SonarQube to Analyze New Container Codebase"

在这一步, Cloud Build会通过`-Dsonar.login=loginHashValue`登录哈希值运行SonarQube, 然后根据当前代码的扫描审查结果与已定义好的SonarQube质量门做比对.

- 当质量门通过时, 这一步返回结果`SUCCESS`
- 当质量门不通过时, 这一步返回结果`FAILED`

在Gradle里, 我们需要加入`--no-daemon`使SonarQube进程能够正常运行.

通过参数`-Dsonar.qualitygate.wait=true`使Cloud Build运行中必须等待SonarQube的Quality Gate结果.

如果目前的代码并不能通过质量门, Cloud Build会根据参数`allow_failure`来决定是否要进行下一步.

像在这里我们定义了`allow_failure: false`, 表明Cloud Build不会允许Pipeline运行中出现错误. 一旦在Pipeline运行过程中的任何一步发生了错误, Cloud Build会直接终止运行, 并返回最终结果`FAILURE`.

如果没有设置参数`allow_failure`, Cloud Build会默认允许错误发生, 且发生后会继续运行, 直到所有的步骤都已完成, 并返回最终结果`SUCCESS`.

---

## 总结

在企业中, 离不开软件项目. 软件又是工程师编写的, 难免会出现代码质量或代码安全问题. 在项目开始初期, 项目团队就应该考虑可能出现的代码问题, 并选择相应的工具来应对. SonarQube是一个无需多虑的选择. 在GCP平台部署k8s的过程中, 将SonarQube整合到CI/CD服务例如Cloud Build, 将是一个比较正确的流程, 再加上正确的工具, 可以在最大程度上保证软件安全无误的运行.

最后, 如果这篇文章对你有帮助, 也欢迎你和我一起交流, 共同进步.
