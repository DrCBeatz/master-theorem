// src/App.tsx
import { useState } from "react";
import "./App.css";
import { MDBCard, MDBCardBody, MDBCardTitle } from "mdb-react-ui-kit";

import Header from "./components/Header/Header";
import AlgorithmForm from "./components/AlgorithmForm/AlgorithmForm";
import FormulaDisplay from "./components/FormulaDisplay/FormulaDisplay";
import ResultDisplay from "./components/ResultDisplay/ResultDisplay";
import AboutMasterTheorem from "./components/AboutMasterTheorem/AboutMasterTheorem";

import { evaluate } from "./services/apiService";

export interface ResultType {
  complexity: string;
  case: string;
  recurrence_relation: string;
  regularity_condition_met?: boolean;
  plot_data: {
    n: number[];
    n_log_b_a: number[];
    f_n: number[];
    time_complexity: number[];
  };
}

export interface AlgorithmType {
  id: number;
  name: string;
  a: number;
  b: number;
  k: number;
  description: string;
  python_code: string;
  case?: string;
  time_complexity?: string;
  complexity_analysis?: string;
}

function App() {
  // State related to inputs (for FormulaDisplay)
  const [a, setA] = useState("");
  const [b, setB] = useState("");
  const [k, setK] = useState("");

  // State related to results
  const [result, setResult] = useState<ResultType | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [selectedAlgorithmDetails, setSelectedAlgorithmDetails] =
    useState<AlgorithmType | null>(null);

  // Handlers to update a, b, k state (needed by FormulaDisplay)
  const handleUpdateA = (newA: string) => setA(newA);
  const handleUpdateB = (newB: string) => setB(newB);
  const handleUpdateK = (newK: string) => setK(newK);

  const handleSubmit = async (
    formA: string,
    formB: string,
    formK: string,
    selectedAlgorithm?: AlgorithmType
  ) => {
    setShowResult(false); // Hide previous results immediately
    setResult(null); // Clear previous result data
    setSelectedAlgorithmDetails(selectedAlgorithm ?? null);

    // Update App's a, b, k state from the submitted form values
    // This ensures FormulaDisplay is up-to-date *after* submission too,
    // although AlgorithmForm already calls the update handlers on change.
    setA(formA);
    setB(formB);
    setK(formK);

    try {
      // Call our service
      const data = await evaluate(formA, formB, formK);
      setResult(data);
      setShowResult(true);
    } catch (error) {
      console.error("There was a problem with your fetch operation:", error);
      setShowResult(false);
    }
  };

  return (
    <>
      <MDBCard alignment="center">
        <Header title="Evaluate Master Theorem" />
        <MDBCardBody>
          <MDBCardTitle>
            <span className="card-title">
              Enter the values of a, b, and k to evaluate the Master Theorem:
            </span>
            {/* Use the new FormulaDisplay component */}
            <FormulaDisplay a={a} b={b} k={k} />
          </MDBCardTitle>

          {/* Pass update handlers and submit handler */}
          <AlgorithmForm
            onSubmit={handleSubmit}
            onUpdateA={handleUpdateA}
            onUpdateB={handleUpdateB}
            onUpdateK={handleUpdateK}
          />
        </MDBCardBody>
      </MDBCard>

      {/* Conditionally render the ResultDisplay component */}
      {showResult && result && (
        <ResultDisplay
          result={result}
          selectedAlgorithmDetails={selectedAlgorithmDetails}
        />
      )}

      {/* Render the static About section */}
      <AboutMasterTheorem />
    </>
  );
}

export default App;
