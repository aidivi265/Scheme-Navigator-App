import { describe, it, expect } from 'vitest';
import { isMatchingState, calculateSchemeMatch, rankSchemesForProfile } from '../services/matchingEngine';
import { Scheme, UserProfile } from '../types';

describe('matchingEngine', () => {
  describe('isMatchingState', () => {
    it('matches All India schemes for any state', () => {
      expect(isMatchingState('Maharashtra', ['All India'])).toBe(true);
      expect(isMatchingState('Uttar Pradesh', ['All India'])).toBe(true);
    });

    it('matches specific states with normalization', () => {
      expect(isMatchingState('Delhi', ['NCT of Delhi'])).toBe(true);
      expect(isMatchingState('Odisha', ['Orissa', 'Odisha'])).toBe(true);
      expect(isMatchingState('Punjab', ['Haryana'])).toBe(false);
    });

    it('handles empty state or coveredStates gracefully', () => {
      expect(isMatchingState('', ['Odisha'])).toBe(false);
      expect(isMatchingState('Bihar', [])).toBe(true);
    });
  });

  describe('calculateSchemeMatch', () => {
    const pmKisan = {
      id: 'pm-kisan',
      slug: 'pm-kisan',
      name: 'PM Kisan Samman Nidhi',
      category: 'Agriculture',
      level: 'Central',
      coveredStates: ['All India'],
      shortDescription: 'Income support to farmer families across India',
      detailedDescription: 'Financial assistance of Rs 6000 per year',
      eligibility: {
        minAge: 18,
        maxAge: 100,
        allowedGenders: ['all'],
        allowedOccupations: ['Farmer'],
      },
      benefits: [{ title: 'Rs 6000 per year' }],
      documents: [{ name: 'Aadhaar Card' }],
      applicationSteps: [{ stepNumber: 1, title: 'Register on portal' }],
      verification: { isOfficialVerified: true },
      popularScore: 98,
      tags: ['farmer', 'agriculture', 'dbt'],
    } as unknown as Scheme;

    const studentProfile: UserProfile = {
      age: 20,
      gender: 'male',
      state: 'Uttar Pradesh',
      occupation: 'Student',
      category: 'General',
      incomeRange: 'Below ₹1 lakh',
      hasBPLCard: false,
    };

    const farmerProfile: UserProfile = {
      age: 45,
      gender: 'male',
      state: 'Uttar Pradesh',
      occupation: 'Farmer',
      category: 'OBC',
      incomeRange: '₹1–2.5 lakh',
      hasBPLCard: false,
    };

    it('gives high match score for eligible farmer on PM-Kisan', () => {
      const result = calculateSchemeMatch(pmKisan, farmerProfile);
      expect(result.matchScore).toBeGreaterThanOrEqual(70);
      expect(result.matchGrade).not.toBe('Not Eligible');
      expect(result.matchedReasons.length).toBeGreaterThan(0);
    });

    it('properly discounts non-matching occupation for student on PM-Kisan', () => {
      const result = calculateSchemeMatch(pmKisan, studentProfile);
      // Student is not a farmer, so score should be low or marked not eligible
      expect(result.matchScore).toBeLessThan(70);
    });
  });

  describe('rankSchemesForProfile', () => {
    const schemes = [
      {
        id: 'pm-kisan',
        slug: 'pm-kisan',
        name: 'PM Kisan',
        category: 'Agriculture',
        level: 'Central',
        coveredStates: ['All India'],
        shortDescription: 'Farmers scheme',
        detailedDescription: 'Farmers scheme',
        eligibility: { allowedOccupations: ['Farmer'] },
        benefits: [],
        documents: [],
        applicationSteps: [],
        verification: { isOfficialVerified: true },
        popularScore: 90,
      },
      {
        id: 'pms-scholarship',
        slug: 'pms-scholarship',
        name: 'Post Matric Scholarship',
        category: 'Education',
        level: 'Central',
        coveredStates: ['All India'],
        shortDescription: 'Student scholarship',
        detailedDescription: 'Student scholarship',
        eligibility: { minAge: 16, maxAge: 30, allowedOccupations: ['Student'] },
        benefits: [],
        documents: [],
        applicationSteps: [],
        verification: { isOfficialVerified: true },
        popularScore: 85,
      },
    ] as unknown as Scheme[];

    it('ranks student scheme highest for a student user', () => {
      const studentProfile: UserProfile = {
        age: 20,
        gender: 'female',
        state: 'Delhi',
        occupation: 'Student',
        category: 'SC',
      };

      const ranked = rankSchemesForProfile(studentProfile, schemes);
      expect(ranked.length).toBeGreaterThan(0);
      expect(ranked[0].scheme.id).toBe('pms-scholarship');
    });
  });
});
