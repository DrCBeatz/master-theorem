// src/components/Header/Header.test.tsx
import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import Header from "./Header";

describe("Header Component", () => {
  it("should render the title passed as a prop inside an h1 tag", () => {
    const testTitle = "My Test Title";
    render(<Header title={testTitle} />);

    // Find the heading element by its role and accessible name (the text content)
    const headingElement = screen.getByRole("heading", {
      name: testTitle,
      level: 1, // Specifies that it should be an <h1>
    });

    // Assert that the element exists in the document
    expect(headingElement).toBeInTheDocument();
  });

  it("should render within an MDB header structure (basic check)", () => {
    const { container } = render(<Header title="Another Title" />);

    const cardHeader = container.querySelector(".card-header");
    expect(cardHeader).toBeInTheDocument();
    expect(cardHeader).toContainElement(
      screen.getByRole("heading", { name: /Another Title/i })
    );
  });
});
