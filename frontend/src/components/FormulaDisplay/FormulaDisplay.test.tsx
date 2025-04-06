// FormulaDisplay.test.tsx
import { describe, it, expect } from "vitest";
import { render, screen } from "@testing-library/react";
import FormulaDisplay from "./FormulaDisplay";

describe("FormulaDisplay component", () => {
  it("displays placeholders for a, b, k when they are empty", () => {
    render(<FormulaDisplay a="" b="" k="" />);

    // Check for partial text "T(n) ="
    expect(screen.getByText(/T\(n\) =/)).toBeInTheDocument();

    // Check for the placeholders 'a', 'b', 'k' as individual nodes
    expect(screen.getByText("a")).toBeInTheDocument();
    expect(screen.getByText("b")).toBeInTheDocument();
    expect(screen.getByText("k")).toBeInTheDocument();
  });

  it("displays the provided values for a, b, k", () => {
    render(<FormulaDisplay a="2" b="3" k="1" />);

    // Check partial text for "T(n) ="
    expect(screen.getByText(/T\(n\) =/)).toBeInTheDocument();

    // Check for the updated numeric values separately
    expect(screen.getByText("2")).toBeInTheDocument();
    expect(screen.getByText("3")).toBeInTheDocument();
    expect(screen.getByText("1")).toBeInTheDocument();

    // (Optional) If you want to confirm the part with `) + f(n` as well:
    // expect(screen.getByText(/\) \+ f\(n/)).toBeInTheDocument();
  });
});
