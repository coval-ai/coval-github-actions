<p align="center">
  <a href="https://www.coval.dev">
    <img src="/content/banner.png" width="100%" alt="Coval" />
  </a>
</p>

<p align="center">
  <strong>🚀 Simulation & evals for voice and chat agents, directly from your CI/CD pipeline.</strong>
</p>

<br />

## :warning: Deprecated

**This repository has been deprecated and is no longer maintained.**

Please use the new repository: **[coval-ai/coval-github-action](https://github.com/coval-ai/coval-github-action)**

---

<br />

<p align="center">
  <a href="https://www.coval.dev">Website</a> •
  <a href="https://docs.coval.dev">Docs</a> •
  <a href="#-github-action">GitHub Action</a> •
</p>

<p align="center">
  <a href="https://github.com/coval-ai/coval-github-actions/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/coval-ai/coval-github-actions" alt="License" />
  </a>
</p>

<br />

Simulation & evals to ship delightful voice & chat AI agents

Coval helps developers build reliable voice and chat agents faster with seamless simulation and evals. Create custom metrics, run 1000s of scenarios, trace workflows and integrate with CI/CD pipelines for actionable insights and peak agent performance.

## 🤖 GitHub Action

Coval offers a GitHub Action to test your agents scripts directly from our CI/CD pipeline. Here's a basic setup of a .github/workflows/run_coval_evaluation.yml:

```yaml
name: Run Coval Evaluation
on:
  workflow_dispatch: # If you want to run the workflow manually
    inputs:
      organization_id:
        description: "Your organization ID."
        required: true
        type: string
      dataset_id:
        description: "Dataset ID to evaluate."
        required: true
        type: string
      created_by:
        description: "Who triggered the workflow."
        required: false
        type: string
      test_set_name:
        description: "Name of the Test Set."
        required: true
        type: string
      config:
        description: "Configuration JSON as a string."
        required: true
        type: string

jobs:
  run-coval-action:
    runs-on: ubuntu-latest
    steps:
      - name: Run Coval Action
        uses: coval-ai/coval-github-actions@v1
        with:
          organization_id: ${{ github.event.inputs.organization_id }}
          dataset_id: ${{ github.event.inputs.dataset_id }}
          created_by: ${{ github.event.inputs.created_by }}
          test_set_name: ${{ github.event.inputs.test_set_name }}
          config: ${{ github.event.inputs.config }}
        env:
          COVAL_API_KEY: ${{ secrets.COVAL_API_KEY }}
```

## Inputs

| Name              | Description                                | Required | Default |
| ----------------- | ------------------------------------------ | -------- | ------- |
| `organization_id` | Your organization ID.                      | Yes      |         |
| `dataset_id`      | The dataset ID to evaluate.                | Yes      |         |
| `created_by`      | Identifier for who triggered the workflow. | No       |         |
| `test_set_name`   | Name of the Test Set to evaluate.          | Yes      |         |
| `config`          | Configuration JSON as a string.            | Yes      |         |

For other configuration options, visit our [GitHub Action documentation](https://docs.coval.dev/getting_started/github_actions_tutorial).

## 📚 Documentation

For detailed guides and API references, visit the [documentation](https://docs.coval.dev).
