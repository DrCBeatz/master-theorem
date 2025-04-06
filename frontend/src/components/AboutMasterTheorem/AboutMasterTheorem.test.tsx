import { describe, it, expect } from "vitest";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import AboutMasterTheorem from "./AboutMasterTheorem";

describe("AboutMasterTheorem component", () => {
  it("renders the main heading", () => {
    render(<AboutMasterTheorem />);
    expect(
      screen.getByRole("heading", { name: /about the master theorem/i })
    ).toBeInTheDocument();
  });

  it("renders the accordion items and their headings", () => {
    render(<AboutMasterTheorem />);
    expect(
      screen.getByText(/what is the master theorem\?/i)
    ).toBeInTheDocument();
    expect(
      screen.getByText(/decoding the master recurrence/i)
    ).toBeInTheDocument();
    expect(
      screen.getByText(/the 3 cases of the master theorem/i)
    ).toBeInTheDocument();
  });

  it("shows content from the first accordion item (which is open by default)", () => {
    render(<AboutMasterTheorem />);
    expect(
      screen.getByText(
        /offers a straightforward way to determine the time complexity/i
      )
    ).toBeInTheDocument();
  });

  it("allows opening the second accordion item", async () => {
    render(<AboutMasterTheorem />);
    const user = userEvent.setup();

    const secondItemPanel = document.getElementById("2");

    // Confirm initially collapsed
    expect(secondItemPanel).not.toHaveClass("show");

    // Click the button
    await user.click(screen.getByText(/decoding the master recurrence/i));

    // Wait for the transition to finish and 'show' to appear
    await waitFor(() => {
      expect(secondItemPanel).toHaveClass("show");
    });
  });
});
