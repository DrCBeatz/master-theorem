// AlgorithmForm.test.tsx
import React from "react";
import { describe, it, expect, vi, beforeEach, afterEach, Mock } from "vitest";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import AlgorithmForm from "./AlgorithmForm";

describe("AlgorithmForm", () => {
  const mockOnSubmit = vi.fn();
  const mockOnUpdateA = vi.fn();
  const mockOnUpdateB = vi.fn();
  const mockOnUpdateK = vi.fn();

  beforeEach(() => {
    // Reset mocks before each test
    mockOnSubmit.mockClear();
    mockOnUpdateA.mockClear();
    mockOnUpdateB.mockClear();
    mockOnUpdateK.mockClear();

    // Mock `fetch` to avoid real network requests
    global.fetch = vi.fn();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("fetches algorithms on mount (no DOM assertion, just confirm fetch called)", async () => {
    (global.fetch as Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => [
        {
          id: 101,
          name: "AlgoOne",
          a: 2,
          b: 2,
          k: 1,
          description: "",
          python_code: "",
        },
        {
          id: 202,
          name: "AlgoTwo",
          a: 3,
          b: 2,
          k: 2,
          description: "",
          python_code: "",
        },
      ],
    });

    render(
      <AlgorithmForm
        onSubmit={mockOnSubmit}
        onUpdateA={mockOnUpdateA}
        onUpdateB={mockOnUpdateB}
        onUpdateK={mockOnUpdateK}
      />
    );

    // Wait for the fetch to complete
    await waitFor(() => expect(global.fetch).toHaveBeenCalledTimes(1));
  });

  it("allows user to type in a, b, k and calls onUpdate handlers", async () => {
    (global.fetch as Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    render(
      <AlgorithmForm
        onSubmit={mockOnSubmit}
        onUpdateA={mockOnUpdateA}
        onUpdateB={mockOnUpdateB}
        onUpdateK={mockOnUpdateK}
      />
    );

    // Find inputs by exact label text
    const aInput = screen.getByLabelText(/a \(number of subproblems\)/i);
    const bInput = screen.getByLabelText(
      /b \(factor to reduce problem size\)/i
    );
    const kInput = screen.getByLabelText(/k \(non-recursive work exponent\)/i);

    // Type numeric values
    await userEvent.type(aInput, "2");
    await userEvent.type(bInput, "3");
    await userEvent.type(kInput, "1");

    // Check that the onUpdate callbacks got called
    expect(mockOnUpdateA).toHaveBeenCalledWith("2");
    expect(mockOnUpdateB).toHaveBeenCalledWith("3");
    expect(mockOnUpdateK).toHaveBeenCalledWith("1");
  });

  it("disables the Evaluate button if any of a, b, or k is empty", async () => {
    (global.fetch as Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    render(
      <AlgorithmForm
        onSubmit={mockOnSubmit}
        onUpdateA={mockOnUpdateA}
        onUpdateB={mockOnUpdateB}
        onUpdateK={mockOnUpdateK}
      />
    );

    const evaluateBtn = screen.getByRole("button", { name: /evaluate/i });

    // Initially all are empty => disabled
    expect(evaluateBtn).toBeDisabled();

    // Fill "a" only
    const aInput = screen.getByLabelText(/a \(number of subproblems\)/i);
    await userEvent.type(aInput, "10");
    expect(evaluateBtn).toBeDisabled(); // b, k still empty

    // Fill "b"
    const bInput = screen.getByLabelText(
      /b \(factor to reduce problem size\)/i
    );
    await userEvent.type(bInput, "2");
    expect(evaluateBtn).toBeDisabled(); // k still empty

    // Fill "k"
    const kInput = screen.getByLabelText(/k \(non-recursive work exponent\)/i);
    await userEvent.type(kInput, "5");

    // Now we have a,b,k => enabled
    expect(evaluateBtn).toBeEnabled();
  });

  it("submits user-entered values and calls onSubmit", async () => {
    (global.fetch as Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => [],
    });

    render(
      <AlgorithmForm
        onSubmit={mockOnSubmit}
        onUpdateA={mockOnUpdateA}
        onUpdateB={mockOnUpdateB}
        onUpdateK={mockOnUpdateK}
      />
    );

    // Fill inputs
    const aInput = screen.getByLabelText(/a \(number of subproblems\)/i);
    const bInput = screen.getByLabelText(
      /b \(factor to reduce problem size\)/i
    );
    const kInput = screen.getByLabelText(/k \(non-recursive work exponent\)/i);

    await userEvent.type(aInput, "2");
    await userEvent.type(bInput, "3");
    await userEvent.type(kInput, "1");

    // Click the Evaluate button
    fireEvent.click(screen.getByRole("button", { name: /evaluate/i }));

    // Check that onSubmit was called with the correct arguments
    expect(mockOnSubmit).toHaveBeenCalledWith("2", "3", "1", undefined);
  });

  it("logs an error when fetchAlgorithms fails", async () => {
    const consoleErrorSpy = vi
      .spyOn(console, "error")
      .mockImplementation(() => {});

    (global.fetch as Mock).mockRejectedValueOnce(new Error("Network error"));

    render(
      <AlgorithmForm
        onSubmit={mockOnSubmit}
        onUpdateA={mockOnUpdateA}
        onUpdateB={mockOnUpdateB}
        onUpdateK={mockOnUpdateK}
      />
    );

    await waitFor(() =>
      expect(console.error).toHaveBeenCalledWith(
        "Failed to fetch algorithms:",
        expect.any(Error)
      )
    );

    consoleErrorSpy.mockRestore();
  });
});
