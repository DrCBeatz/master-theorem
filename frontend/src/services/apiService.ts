// frontend/src/services/apiService.ts

import { ResultType, AlgorithmType } from "../App";

const API_BASE_URL = import.meta.env.VITE_API_URL;

/**
 * Makes a POST request to /evaluate
 * @param a
 * @param b
 * @param k
 * @returns Promise<ResultType>
 */
export async function evaluate(
  a: string,
  b: string,
  k: string
): Promise<ResultType> {
  const response = await fetch(`${API_BASE_URL}/evaluate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ a, b, k }),
  });

  if (!response.ok) {
    throw new Error(`Network response was not ok: ${response.statusText}`);
  }
  return response.json();
}

/**
 * Makes a GET request to /algorithms
 * @returns Promise<AlgorithmType[]>
 */
export async function getAlgorithms(): Promise<AlgorithmType[]> {
  const response = await fetch(`${API_BASE_URL}/algorithms`);
  if (!response.ok) {
    throw new Error(`Network response was not ok: ${response.statusText}`);
  }
  return response.json();
}
