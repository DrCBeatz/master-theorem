// ResultDisplay.test.tsx

import React from "react";
import { describe, it, expect, beforeEach, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import ResultDisplay from "./ResultDisplay";
import { ResultType, AlgorithmType } from "../../App";

// 1) Mock out chart.js to avoid canvas issues
vi.mock("chart.js/auto", () => {
  const FakeChart = vi.fn(() => ({
    destroy: vi.fn(),
  }));
  return {
    // The "Chart" constructor
    default: FakeChart,
  };
});

describe("ResultDisplay component", () => {
  let mockResult: ResultType;

  beforeEach(() => {
    // Minimal result object that satisfies your interface
    mockResult = {
      recurrence_relation: "T(n) = 2T(n/2) + n",
      case: "Case 1: O(n log n)",
      complexity: "O(n log n)",
      plot_data: {
        n: [1, 2, 4, 8],
        n_log_b_a: [1, 2, 4, 8],
        f_n: [1, 2, 4, 8],
        time_complexity: [1, 2, 4, 8],
      },
    };
  });

  it("displays the regularity condition text if case includes Case 3", () => {
    // Modify our mock to use "Case 3: Θ(n^k)" so that condition is relevant
    mockResult.case = "Case 3: Θ(n<sup>k</sup>)";
    mockResult.regularity_condition_met = false;

    render(
      <ResultDisplay result={mockResult} selectedAlgorithmDetails={null} />
    );

    // Should see text "Regularity Condition Met:"
    // and a "No" because regularity_condition_met is false
    expect(screen.getByText(/Regularity Condition Met:/i)).toBeInTheDocument();
    expect(screen.getByText("No")).toBeInTheDocument();
  });

  it("shows selected algorithm details when selectedAlgorithmDetails is provided", () => {
    const mockAlgorithm: AlgorithmType = {
      id: 1,
      name: "Merge Sort",
      a: 2,
      b: 2,
      k: 1,
      description: "Divide and conquer sorting algorithm",
      python_code: "def merge_sort(arr): pass",
    };

    render(
      <ResultDisplay
        result={mockResult}
        selectedAlgorithmDetails={mockAlgorithm}
      />
    );

    // The h4 with the algorithm name
    expect(
      screen.getByRole("heading", { name: /merge sort algorithm/i })
    ).toBeInTheDocument();

    // The accordion items
    expect(screen.getByText(/Algorithm Description/i)).toBeInTheDocument();
    expect(
      screen.getByText(/Divide and conquer sorting algorithm/i)
    ).toBeInTheDocument();

    expect(screen.getByText(/Python Code/i)).toBeInTheDocument();
    expect(
      screen.getByText(/def merge_sort\(arr\): pass/i)
    ).toBeInTheDocument();
  });
});
