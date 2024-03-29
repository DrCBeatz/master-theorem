// frontend/src/components/Header/Header.test.tsx

import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import Header from "./Header";

describe("Header", () => {
  test("renders the title prop correctly", () => {
    const testTitle = "Evaluate Master Theorem";
    render(<Header title={testTitle} />);
    const headingElement = screen.getByRole("heading", { name: testTitle });
    expect(headingElement).toBeInTheDocument();
  });
});
