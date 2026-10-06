import test from 'node:test';
import assert from 'node:assert/strict';
import { normalize } from './jev.js';

test('low confidence goes to human', () => assert.equal(normalize({ category: 'routine', action: 'archive', confidence: 40 }).needsHuman, true));
test('delete always needs a human', () => assert.equal(normalize({ category: 'spam', action: 'delete', confidence: 99 }).needsHuman, true));
test('invalid model output is sanitized', () => {
  const r = normalize({ category: 'bogus', action: 'nuke', confidence: 'x' });
  assert.deepEqual([r.category, r.action, r.confidence], ['routine', 'snooze', 0]);
});
