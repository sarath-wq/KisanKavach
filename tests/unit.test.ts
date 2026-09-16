import test from 'node:test';
import assert from 'node:assert';
import { calculateSLA } from '../src/lib/sla/engine';
import { analyzeFraudRisk } from '../src/lib/fraud/analyzer';

test('SLA Engine - Normal SLA Calculation', () => {
  const submittedAt = new Date(Date.now() - 3 * 24 * 60 * 60 * 1000); // 3 days ago
  const sla = calculateSLA(submittedAt, 7);
  assert.strictEqual(sla.elapsedDays, 3);
  assert.strictEqual(sla.remainingDays, 4);
  assert.strictEqual(sla.isBreached, false);
  assert.strictEqual(sla.statusColor, 'GREEN');
});

test('SLA Engine - Breached SLA Calculation', () => {
  const submittedAt = new Date(Date.now() - 9 * 24 * 60 * 60 * 1000); // 9 days ago
  const sla = calculateSLA(submittedAt, 7);
  assert.strictEqual(sla.elapsedDays, 9);
  assert.strictEqual(sla.remainingDays, 0);
  assert.strictEqual(sla.isBreached, true);
  assert.strictEqual(sla.statusColor, 'RED');
});

test('Fraud Risk Analyzer - Detect High Risk Phishing Link & OTP Request', () => {
  const text = 'Urgent! Your KCC loan is approved. Share OTP and click http://bit.ly/kcc-phish to claim.';
  const analysis = analyzeFraudRisk(text);
  assert.strictEqual(analysis.riskLevel, 'HIGH');
  assert.strictEqual(analysis.isPhishing, true);
  assert.ok(analysis.riskScore >= 75);
});

test('Fraud Risk Analyzer - Legitimate Branch Notice', () => {
  const text = 'Dear Farmer, please visit your local bank branch to complete routine documentation.';
  const analysis = analyzeFraudRisk(text);
  assert.strictEqual(analysis.riskLevel, 'LOW');
  assert.strictEqual(analysis.isPhishing, false);
});
