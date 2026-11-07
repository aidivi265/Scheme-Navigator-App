import { describe, it, expect, beforeEach } from 'vitest';
import {
  getSavedSchemes,
  saveScheme,
  removeSavedScheme,
  toggleSaveScheme,
  getTrackerItems,
  saveTrackerItem,
  updateTrackerStatus,
  removeTrackerItem,
  getAuthUser,
  setAuthUser,
  getAuthToken,
  logoutUser,
  clearAllUserData,
} from '../services/storageService';
import { Scheme } from '../types';

describe('storageService', () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.clear();
    clearAllUserData();
  });

  const mockScheme = {
    id: 'test-scheme-1',
    slug: 'test-scheme-1',
    name: 'Test Scheme',
    category: 'Education',
    level: 'Central',
    shortDescription: 'Test Description',
    detailedDescription: 'Detailed test description',
    eligibility: {},
    benefits: [],
    documents: [],
    applicationSteps: [],
    verification: { isOfficialVerified: true },
    popularScore: 50,
  } as unknown as Scheme;

  it('saves and retrieves saved schemes', () => {
    saveScheme(mockScheme);
    const saved = getSavedSchemes();
    expect(saved.length).toBe(1);
    expect(saved[0].id).toBe('test-scheme-1');
  });

  it('toggles saving schemes properly', () => {
    const isSavedFirst = toggleSaveScheme(mockScheme);
    expect(isSavedFirst).toBe(true);
    expect(getSavedSchemes().length).toBe(1);

    const isSavedSecond = toggleSaveScheme(mockScheme);
    expect(isSavedSecond).toBe(false);
    expect(getSavedSchemes().length).toBe(0);
  });

  it('removes saved scheme correctly', () => {
    saveScheme(mockScheme);
    removeSavedScheme(mockScheme);
    expect(getSavedSchemes().length).toBe(0);
  });

  it('updates and retrieves application tracker items', () => {
    updateTrackerStatus(
      'test-scheme-1',
      'Test Scheme',
      'Education' as any,
      'Ready to Apply',
      'Initial application note'
    );

    const items = getTrackerItems();
    expect(items.length).toBe(1);
    expect(items[0].schemeId).toBe('test-scheme-1');
    expect(items[0].status).toBe('Ready to Apply');
    expect(items[0].notes).toBe('Initial application note');

    // Update status to 'Applied Externally'
    updateTrackerStatus(
      'test-scheme-1',
      'Test Scheme',
      'Education' as any,
      'Applied Externally',
      'Application submitted successfully'
    );

    const updated = getTrackerItems();
    expect(updated.length).toBe(1);
    expect(updated[0].status).toBe('Applied Externally');

    // Remove tracker item
    removeTrackerItem('test-scheme-1');
    expect(getTrackerItems().length).toBe(0);
  });

  it('manages auth user and signed token securely', () => {
    setAuthUser({
      id: 'usr-1',
      name: 'Ramesh Kumar',
      email: 'ramesh@example.com',
      isLoggedIn: true,
      token: 'signed-cryptographic-token-xyz',
    });

    const user = getAuthUser();
    expect(user).not.toBeNull();
    expect(user?.name).toBe('Ramesh Kumar');
    expect(getAuthToken()).toBe('signed-cryptographic-token-xyz');

    logoutUser();
    expect(getAuthUser()).toBeNull();
    expect(getAuthToken()).toBe('');
  });
});
