// frontend/tests/test-setup.ts

import "@testing-library/jest-dom";
import ResizeObserver from "resize-observer-polyfill";
import { vi } from "vitest";

class MockChart {
  constructor(ctx: CanvasRenderingContext2D, config: any) {
  }
  destroy() {
  }
}

vi.mock("chart.js/auto", () => {
  return {
    default: MockChart,
  };
});

Object.defineProperty(HTMLCanvasElement.prototype, "getContext", {
  value: function () {
    return {
      fillRect: () => {},
      clearRect: () => {},
      getImageData: () => ({ data: [] }),
      putImageData: () => {},
      createImageData: () => [],
      setTransform: () => {},
      drawImage: () => {},
      save: () => {},
      fillText: () => {},
      restore: () => {},
      beginPath: () => {},
      moveTo: () => {},
      lineTo: () => {},
      closePath: () => {},
      stroke: () => {},
      translate: () => {},
      scale: () => {},
      rotate: () => {},
      arc: () => {},
      fill: () => {},
      measureText: () => ({ width: 0 }),
      transform: () => {},
    };
  },
});

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

// Make Vitest/JSDOM aware of ResizeObserver:
if (!global.ResizeObserver) {
  global.ResizeObserver = ResizeObserver;
}
