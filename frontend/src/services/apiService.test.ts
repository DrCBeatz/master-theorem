// apiService.test.ts

import { describe, it, expect, beforeEach, vi } from "vitest";
import { evaluate, getAlgorithms } from "./apiService";

// A helper function to mock the fetch response easily
const mockFetch = (status: number, data: any) => {
  return vi.fn().mockResolvedValue({
    ok: status >= 200 && status < 300,
    status,
    statusText: status !== 200 ? "Error" : "OK",
    json: async () => data,
  });
};

describe("apiService", () => {
  beforeEach(() => {
    // Reset all mocks before each test
    vi.resetAllMocks();
  });

  describe("evaluate", () => {
    it("should make a POST request and return the JSON result on success", async () => {
      // Arrange: Mock fetch to return a 200 status with expected data
      const mockResponseData = { solution: "O(n log n)" };
      global.fetch = mockFetch(200, mockResponseData);

      // Act: Call the function under test
      const result = await evaluate("2", "n/2", "1");

      // Assert: Check that fetch was called correctly
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("/evaluate"), // the URL
        expect.objectContaining({
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ a: "2", b: "n/2", k: "1" }),
        })
      );
      expect(result).toEqual(mockResponseData);
    });

    it("should throw an error if the response is not ok", async () => {
      // Arrange: Mock fetch to return a 400 status
      global.fetch = mockFetch(400, { error: "Bad Request" });

      // Act & Assert: We expect an error to be thrown
      await expect(evaluate("2", "n/2", "1")).rejects.toThrow(
        "Network response was not ok: Error"
      );
    });
  });

  describe("getAlgorithms", () => {
    it("should make a GET request and return an array of AlgorithmType", async () => {
      // Arrange: Mock fetch to return a 200 status with some sample data
      const mockAlgorithms = [
        { id: 1, name: "Merge Sort", complexity: "O(n log n)" },
      ];
      global.fetch = mockFetch(200, mockAlgorithms);

      // Act
      const algorithms = await getAlgorithms();

      // Assert
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining("/algorithms")
      );
      expect(algorithms).toEqual(mockAlgorithms);
    });

    it("should throw an error if the response is not ok", async () => {
      // Arrange: Mock fetch to return a 500 status
      global.fetch = mockFetch(500, { error: "Server Error" });

      // Act & Assert
      await expect(getAlgorithms()).rejects.toThrow(
        "Network response was not ok: Error"
      );
    });
  });
});
