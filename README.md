# Quantitative Risk & Performance Metrics in Python

This repository contains Python implementations of commonly used quantitative risk and performance metrics applied to financial return series.

The models focus on measuring downside risk, tail risk, risk-adjusted returns, and historical loss characteristics — core concepts in portfolio management and risk analysis.

## Implemented Metrics

### Value at Risk (VaR)

Value at Risk (VaR) estimates the maximum expected loss over a specified time horizon at a given confidence level.

VaR provides a standardized measure of downside exposure and is widely used in risk management, capital allocation, and regulatory frameworks.

---

### Conditional Value at Risk (CVaR / Expected Shortfall)

Conditional Value at Risk (CVaR), also known as Expected Shortfall (ES), measures the expected loss given that losses exceed the VaR threshold.

Unlike VaR, CVaR captures tail risk and extreme loss scenarios, making it more informative during periods of market stress.

---

### Sortino Ratio

The Sortino Ratio is a downside-risk-adjusted performance metric that evaluates returns relative to negative volatility only.

By penalizing harmful deviations instead of total volatility, it provides a clearer view of risk-adjusted performance.

---

### Maximum Drawdown (MDD)

Maximum Drawdown (MDD) measures the largest observed decline from a peak value to a subsequent trough.

It is a path-dependent risk metric used to evaluate worst-case historical losses and strategy robustness.

---

## Purpose

These implementations are designed for analytical and educational use, illustrating standard quantitative techniques used in financial risk assessment and performance evaluation.

## Notes

The models operate on historical price or return data and can be applied to any tradable financial instrument, including equities, ETFs, indices, or systematic trading strategies.

While commonly used in portfolio analysis, these metrics are equally valid for evaluating the risk and performance characteristics of individual assets.
