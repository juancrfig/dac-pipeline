# Hackathon Submission: Hermes Agent Creative Hackathon

## Event

- **Name**: Hermes Agent Creative Hackathon
- **Dates**: 16 days
- **Prizes**: $25,000
- **Sponsors**: Kimi Moonshot AI, Nous Research
- **Theme**: Creative domains — video, image, audio, 3D, long-form writing, creative software, interactive media

## Why DAC Fits

At first glance, "documentation CI pipeline" doesn't sound creative. But the creative angle is in **what this enables**:

### The Real Problem for Creative Coders

Creative projects are the hardest for AI assistants to understand:

- **Game engines**: Complex architecture (render loop, physics, entity systems), rapid refactoring
- **Generative art**: p5.js/Three.js pipelines with heavy shader code, asset pipelines
- **Audio tools**: DSP chains, real-time constraints, plugin architectures
- **Interactive media**: State machines, event systems, hardware integrations

When docs drift in these projects, AI assistants don't just write wrong code — they break the creative vision. A stale reference to a renamed shader file means a broken visual effect. An outdated function signature in audio DSP means glitching output.

### What DAC Enables

| Creative Domain | What DAC Protects |
|-----------------|-----------------|
| Game dev | Engine architecture docs stay synced with actual render/physics systems |
| Generative art | p5.js/Three.js pipeline docs match current shader/asset structure |
| Audio tools | DSP function signatures in docs match actual audio chain code |
| Interactive media | State machine docs reflect current event flow |
| 3D pipelines | Asset pipeline documentation matches actual import/export code |

### The Creative Angle

> **"Less time fixing AI mistakes → more time creating."**

DAC isn't the creative tool. It's the **infrastructure that keeps creative tools working** when AI assistants are involved.

In a hackathon context, teams using Hermes Agent to build creative projects will hit doc drift within hours. DAC ensures their AI assistant stays accurate throughout the 16-day sprint.

### Demo Idea for Hackathon

1. Take a creative project (e.g., a generative art tool built with Hermes)
2. Show AGENTS.md going stale after a few refactors
3. Show AI assistant making wrong assumptions
4. Install DAC
5. Show CI catching drift before merge
6. Show AI assistant now working correctly

## Submission Details

- **Project**: DAC (Docs-as-Code Pipeline)
- **Repo**: https://github.com/juancrfig/dac-pipeline
- **Built with**: Python, Tree-sitter, GitHub Actions
- **Integrates with**: Hermes Agent (first dogfood user)
- **Category**: Infrastructure for creative AI workflows

## Judges' Criteria Alignment

| Criterion | How DAC Addresses |
|-----------|-------------------|
| Creativity | Solves a novel problem (doc drift for AI assistants) |
| Technical depth | AST parsing, multi-language support, CI integration |
| Impact | Every AI-assisted project benefits |
| Hermes integration | First-class support, dogfooded on Hermes itself |

## Team

- Juanes Figueroa — Founder, engineer

---

*Submitted for the Hermes Agent Creative Hackathon 2026.*
