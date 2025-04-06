import React from "react";
import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { act } from "@testing-library/react";
import App from "./App";
import * as apiService from "./services/apiService";

const mockResult = {
  complexity: "O(n)",
  case: "Case 2",
  recurrence_relation: "T(n) = 2T(n/2) + n^1",
  plot_data: {
    n: [],
    n_log_b_a: [],
    f_n: [],
    time_complexity: [],
  },
};

describe("App component", () => {
  beforeEach(() => {
    vi.spyOn(apiService, "evaluate").mockResolvedValue(mockResult);
    vi.spyOn(apiService, "getAlgorithms").mockResolvedValue([
      {
        id: 1,
        name: "Mock Algorithm",
        a: 2,
        b: 2,
        k: 1,
        description: "Mock Description",
        python_code: "print('Mock')",
      },
    ]);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("renders the header with 'Evaluate Master Theorem'", async () => {
    render(<App />);

    await screen.findByRole("heading", { name: /Evaluate Master Theorem/i });

    const heading = screen.getByRole("heading", {
      name: /Evaluate Master Theorem/i,
    });
    expect(heading).toBeInTheDocument();
  });

  it("disables the 'Evaluate' button if inputs are empty", async () => {
    await act(async () => {
      render(<App />);
    });

    const evaluateButton = screen.getByRole("button", { name: /evaluate/i });
    expect(evaluateButton).toBeDisabled();
  });

  it("loads algorithm list on mount and allows selecting an algorithm", async () => {
    render(<App />);

    await waitFor(() => {
      expect(apiService.getAlgorithms).toHaveBeenCalledTimes(1);
    });

    const algorithmSelect = screen.getByTestId("algorithm-select");
    expect(algorithmSelect).toBeInTheDocument();
  });

  it("submits the form and displays results when user inputs are provided", async () => {
    render(<App />);

    // Input fields
    const aInput = screen.getByLabelText("a (number of subproblems)");
    const bInput = screen.getByLabelText("b (factor to reduce problem size)");
    const kInput = screen.getByLabelText("k (non-recursive work exponent)");
    const evaluateButton = screen.getByRole("button", { name: /evaluate/i });

    // Fill in the form
    fireEvent.change(aInput, { target: { value: "2" } });
    fireEvent.change(bInput, { target: { value: "2" } });
    fireEvent.change(kInput, { target: { value: "1" } });

    // The button should now be enabled
    expect(evaluateButton).not.toBeDisabled();

    // Submit the form
    fireEvent.click(evaluateButton);

    // Wait for the API call to complete and for the result to display
    await waitFor(() => {
      // The `evaluate` function should have been called once with these args
      expect(apiService.evaluate).toHaveBeenCalledWith("2", "2", "1");
      expect(apiService.evaluate).toHaveBeenCalledTimes(1);
    });

    // Check the displayed complexity text (from your mock)
    expect(screen.getByText(/O\(n\)/i)).toBeInTheDocument();
    // Or check for other parts of the mock result
    expect(screen.getByTestId("evaluation-case")).toHaveTextContent(/Case 2/i);
  });
});
