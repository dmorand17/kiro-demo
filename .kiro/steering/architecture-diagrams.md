---
title: Architecture Diagrams
inclusion: never
---

# Architecture Diagrams

## Overview

Architecture diagrams are automatically generated using the AWS Diagram MCP server based on Terraform infrastructure definitions. Diagrams provide visual documentation of the deployed AWS resources and their relationships.

## Diagram Generation

### When to Generate

- After modifying Terraform files (.tf)
- When adding new AWS resources
- After infrastructure changes are applied
- During documentation updates

### Generation Process

1. Scan current Terraform configuration files
2. Identify AWS resources and their relationships
3. Use AWS Diagram MCP server to generate diagram

## Diagram Standards

### Layout

- **Direction**: Left-to-right (LR) for request flow
- **Start Point**: User or client on the left
- **End Point**: Data storage or response on the right
- **Grouping**: Use Clusters for related resources

### Naming Conventions

- Use actual resource names from Terraform
- Include runtime/version info (e.g., "Python 3.13")
- Add key configuration details (e.g., "7-day retention")
- Format: `{resource-name}\n({details})`

## File Organization

### Storage Location

- **Naming**: `{project-name}-{diagram-type}`
- **Example**: `hello-world-lambda-architecture`

### Version Control

- Commit generated diagrams to Git
- Update diagrams before committing infrastructure changes
- Include diagram updates in the same commit as Terraform changes

## Best Practices

- **Simplicity**: Only show relevant resources
- **Clarity**: Use clear labels and grouping
- **Consistency**: Follow naming conventions
- **Accuracy**: Match actual Terraform configuration
- **Updates**: Regenerate after infrastructure changes
- **Documentation**: Include key configuration details in labels
