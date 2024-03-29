// test-setup.ts

import "@testing-library/jest-dom";

class MockIntersectionObserver {
  root: Element | null = null;
  rootMargin: string = "";
  thresholds: ReadonlyArray<number> = [];
  observe: (target: Element) => void = () => {};
  unobserve: (target: Element) => void = () => {};
  disconnect: () => void = () => {};
  takeRecords: () => IntersectionObserverEntry[] = () => [];
}

Object.defineProperty(window, "IntersectionObserver", {
  writable: true,
  configurable: true,
  value: MockIntersectionObserver,
});
