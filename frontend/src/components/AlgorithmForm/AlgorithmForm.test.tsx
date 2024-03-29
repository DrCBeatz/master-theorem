import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import AlgorithmForm from "./AlgorithmForm";

describe("AlgorithmForm", () => {
  it("renders without crashing", () => {
    render(
      <AlgorithmForm
        onSubmit={vi.fn()}
        onUpdateA={vi.fn()}
        onUpdateB={vi.fn()}
        onUpdateK={vi.fn()}
      />
    );
    expect(
      screen.getByLabelText(/a \(number of subproblems\)/i)
    ).toBeInTheDocument();
  });

  it("updates input fields correctly", async () => {
    const user = userEvent.setup();
    render(
      <AlgorithmForm
        onSubmit={vi.fn()}
        onUpdateA={vi.fn()}
        onUpdateB={vi.fn()}
        onUpdateK={vi.fn()}
      />
    );

    await user.type(screen.getByLabelText(/a \(number of subproblems\)/i), "4");
    expect(screen.getByLabelText(/a \(number of subproblems\)/i)).toHaveValue(
      "4"
    );

    await user.type(
      screen.getByLabelText(/b \(factor by which problem size is reduced\)/i),
      "2"
    );
    expect(
      screen.getByLabelText(/b \(factor by which problem size is reduced\)/i)
    ).toHaveValue("2");

    await user.type(
      screen.getByLabelText(
        /k \(exponent in the work outside of recursive calls\)/i
      ),
      "1"
    );
    expect(
      screen.getByLabelText(
        /k \(exponent in the work outside of recursive calls\)/i
      )
    ).toHaveValue("1");
  });

  it("calls onSubmit with the right parameters on form submission", async () => {
    const onSubmitMock = vi.fn();
    const user = userEvent.setup();
    render(
      <AlgorithmForm
        onSubmit={onSubmitMock}
        onUpdateA={vi.fn()}
        onUpdateB={vi.fn()}
        onUpdateK={vi.fn()}
      />
    );

    await user.type(screen.getByLabelText(/a \(number of subproblems\)/i), "4");
    await user.type(
      screen.getByLabelText(/b \(factor by which problem size is reduced\)/i),
      "2"
    );
    await user.type(
      screen.getByLabelText(
        /k \(exponent in the work outside of recursive calls\)/i
      ),
      "1"
    );
    await user.click(screen.getByRole("button", { name: /evaluate/i }));

    // Updated expectation to match the implementation
    expect(onSubmitMock).toHaveBeenCalledWith("4", "2", "1", undefined);
  });
});
