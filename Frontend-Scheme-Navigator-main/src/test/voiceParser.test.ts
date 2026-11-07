import { describe, it, expect } from 'vitest';
import { parseVoiceInput, calculateIncomeRange } from '../utils/voiceParser';

describe('voiceParser', () => {
  it('correctly calculates income ranges', () => {
    expect(calculateIncomeRange(50000)).toBe('Below ₹1 lakh');
    expect(calculateIncomeRange(150000)).toBe('₹1–2.5 lakh');
    expect(calculateIncomeRange(350000)).toBe('₹2.5–5 lakh');
    expect(calculateIncomeRange(750000)).toBe('₹5–10 lakh');
    expect(calculateIncomeRange(1200000)).toBe('₹10 lakh+');
  });

  it('parses age and gender from spoken English', () => {
    const res = parseVoiceInput('I am a 28 year old woman living in Delhi');
    expect(res.profile.age).toBe(28);
    expect(res.profile.gender).toBe('female');
    expect(res.profile.state).toBe('Delhi');
  });

  it('parses Hindi voice input for farmer and BPL', () => {
    const res = parseVoiceInput('main uttar pradesh ka kisan hoon meri umar 45 saal hai bpl card hai');
    expect(res.profile.state).toBe('Uttar Pradesh');
    expect(res.profile.occupation).toBe('Farmer');
    expect(res.profile.age).toBe(45);
    expect(res.profile.hasBPLCard).toBe(true);
  });

  it('parses student occupation from voice input', () => {
    const res = parseVoiceInput('I am a college student from Maharashtra looking for scholarship');
    expect(res.profile.occupation).toBe('Student');
    expect(res.profile.state).toBe('Maharashtra');
  });

  it('handles empty or unrecognized input safely', () => {
    const res = parseVoiceInput('');
    expect(res.profile).toEqual({});
    expect(res.entities).toEqual([]);
  });
});
