# Learning GitOps

GitOps 를 통한 배포를 알아보기 위한 자료입니다. 로컬 환경과 GitHub 계정으로 모두 동작하고, Argo CD 를 통해 GitOps 배포를 관리합니다.

실습은 [여기](https://www.notion.so/healingpaper/GitOps-16d48d642b424b5db88455f4f568bedd?pvs=4)에서 확인할 수 있습니다.

## 디렉토리 레이아웃

```
.
├── gitops
│   ├── applications
│   │   ├── coffee
│   │   │   ├── cart
│   │   │   │   ├── api
│   │   │   │   └── secret
│   │   │   └── order
│   │   │       ├── api
│   │   │       └── secret
│   │   └── platform
│   │       ├── argo-cd
│   │       ├── argo-resources
│   │       ├── argo-rollouts
│   │       ├── external-secrets
│   │       └── metrics-server
│   ├── bootstrap
│   │   ├── phase-0
│   │   ├── phase-1
│   │   ├── phase-2
│   │   ├── phase-3
│   │   └── phase-4
│   ├── charts
│   │   └── mini
│   └── products
│       └── coffee
└── products
    └── coffee
        ├── cart
        │   └── api
        │       ├── src
        │       └── tests
        └── order
            └── api
                ├── src
                └── tests
```

최상위에는 `gitops` 와 `products` 로 나뉩니다. 일반적으로 어플리케이션 소스 레포지토리와 GitOps 배포 레포지토리는 다르게 하라고 하지만, 여기서는 학습의 편의를 위해 하나의 레포지토리에서 최상위 폴더로 구분합니다. `gitops` 는 GitOps 배포 코드, `products` 의 `coffee` 는 샘플 제품인 커피샾의 코드를 담고 있습니다.

`gitops` 아래에 있는 `bootstrap` 부터 보겠습니다. Phase 0 에서 랩탑에 [`kind`](https://kind.sigs.k8s.io/) 를 통해 쿠버네티스를 설치합니다. Phase 1 에서는 Argo CD 를 손으로 설치하고, Phase 2 에서는 GitOps 에서 추구하는 선언적 리소스 관리를 위해 Argo CD 자체를 Argo CD 어플리케이션으로 등록합니다. Phase 3 에서는 서비스의 제공을 위해 필요한 여러 외부 제품을 쿠버네티스 클러스터 위에 Argo CD 어플리케이션으로 등록하고 설치합니다. 여기서는 오토 스케일링을 위한 [Metrics Server](https://github.com/kubernetes-sigs/metrics-server), 시크릿 주입을 위한 [External Secrets Operator](https://external-secrets.io/latest/) 를 설치합니다. Phase 4 에서는 우리가 만드는 제품을 Argo CD 어플리케이션으로 등록합니다.

`gitops` 아래에 있는 `charts` 는 내부에서 사용할 헬름 챠트를 제공합니다. 한 조직에서 대부분 비슷한 형태로 배포하게 되므로, 배포의 편의를 위해 헬름 챠트를 등록해서 공용으로 사용합니다. 여기서는 `mini` 라는 이름의, 미니서비스의 의미를 담은 챠트를 하나 가지고 있습니다.

`gitops` 아래에 있는 `products` 는 내부에서 만드는 제품을 관리하고 Argo CD 어플리케이션을 자동으로 만듭니다.

`products` 아래에는 제품 이름으로 첫 디렉토리가 나뉘며, 여기서는 `coffee` 만 있습니다. 그 아래 여러 어플리케이션의 소스가 등록됩니다.

## Argo 어플리케이션 셋을 통한 어플리케이션 자동 배포

`gitops/products` 아래에는 `coffee` 라는 제품이 등록되어 있습니다. 그 아래 `application-set.yaml` 에 Argo 어플리케이션 셋이 만들어집니다. 이 리소스의 역할은 다음과 같습니다.

- `gitops/applications/coffee/*` 디렉토리의 구조를 계속 모니터링합니다. 예를들어 `payment` 라는 새로운 디렉토리가 생겨나거나, `cart` 라는 디렉토리가 삭제되었다면, 이를 감지합니다.
- 디렉토리의 변경에 맞춰서 Argo 어플리케이션을 변경합니다. 새로 `payment` 디렉토리가 생겼다면, 이 이름으로 Argo 어플리케이션을 만들고, `cart` 디렉토리가 삭제되었다면, 이 이름의 Argo 어플리케이션과 쿠버네티스 리소스를 제거합니다.

> [!NOTE]
> 삭제, 생성 등의 자동 동기화는 설정이 가능합니다. 여기서는 모든 리소스의 생성과 삭제 모두 자동으로 동기화되어 동작하도록 되어있습니다. 이는 `syncPolicy` 설정을 통해 조절이 가능합니다.

`gitops/applications` 아래에는 제품과 서비스 이름으로 폴더가 나뉘어집니다. 그리고 그 아래 쿠버네티스에 배포하기 위한 매니페스트가 있습니다. 모든 리소스는 서비스 이름 단위로 Argo CD 어플리케이션이 만들어집니다. 그 하위 모든 매니페스트는 하나의 Argo CD 배포로 합쳐져서 배포됩니다.

단, Argo 어플리케이션 셋의 특성 상, 하나의 어플리케이션 셋으로 묶였다면 하나의 쿠버네티스 자원 배포 방식만 설정이 가능합니다. 어떤 디렉토리에서는 헬름으로, 어떤 디렉토리에서는 커스터마이즈로 하는 등의 설정은 불가능합니다. 그래서 여기서는 모든 배포는 커스터마이즈로 하고, 헬름도 커스터마이즈로 한 번 감싸서 배포합니다. 이를 위해 Argo CD 배포 시 Argo CD 컨피그맵에 `kustomize.buildOptions: "--enable-helm"` 를 반드시 추가해줘야 합니다.
