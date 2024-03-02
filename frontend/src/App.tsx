// frontend/src/App.tsx

import { useState } from "react";
import "./App.css";
import {
  MDBCard,
  MDBCardBody,
  MDBCardTitle,
  MDBCardText,
  MDBCardHeader,
  MDBBtn,
  MDBInput,
} from "mdb-react-ui-kit";

interface ResultType {
  complexity: string;
  case: string;
  plot_url: string;
}

function App() {
  const [a, setA] = useState("");
  const [b, setB] = useState("");
  const [k, setK] = useState("");
  const [result, setResult] = useState<ResultType | null>(null);
  const [showResult, setShowResult] = useState(false);

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const handleSubmit = async (event: React.MouseEvent<any>) => {
    event.preventDefault(); // Prevent default form submission behavior
    setShowResult(false);

    try {
      const response = await fetch("http://localhost:8000/api/evaluate/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ a, b, k }),
      });

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }

      const data = await response.json();
      setResult(data);
      setShowResult(true);
    } catch (error) {
      console.error("There was a problem with your fetch operation:", error);
    }
  };

  return (
    <>
      <MDBCard alignment="center">
        <MDBCardHeader>
          <h1>Evaluate Master Theorem</h1>
        </MDBCardHeader>
        <MDBCardBody>
          <MDBCardTitle>
            Enter the values of a, b, and k to evaluate the Master Theorem
          </MDBCardTitle>
          <MDBInput
            label="a (number of subproblems)"
            id="aInput"
            type="number"
            min="1"
            className="my-4"
            value={a}
            onChange={(e) => setA(e.target.value)}
          />
          <MDBInput
            label="b (factor by which the problem size is reduced)"
            id="bInput"
            type="number"
            min="2"
            className="my-4"
            value={b}
            onChange={(e) => setB(e.target.value)}
          />
          <MDBInput
            label="k (exponent in the work done outside the recursive calls)"
            id="kInput"
            type="number"
            min="0"
            className="my-4"
            value={k}
            onChange={(e) => setK(e.target.value)}
          />

          <MDBBtn onClick={handleSubmit} className="btn-block">
            Evaluate
          </MDBBtn>
        </MDBCardBody>
      </MDBCard>

      {showResult && result && (
        <MDBCard className="my-5">
          <MDBCardHeader>
            <h2>Evaluation</h2>
          </MDBCardHeader>
          <MDBCardBody>
            <img
              src={result.plot_url}
              className="img-fluid"
              alt="Master Theorem Evaluation"
            />
            <MDBCardText>
              <p>
                <strong>Time Complexity: </strong> {result.complexity})
              </p>
            </MDBCardText>
            <MDBCardText>
              <p>
                <strong>Evaluation: </strong> {result.case}
              </p>
            </MDBCardText>
          </MDBCardBody>
        </MDBCard>
      )}
    </>
  );
}

export default App;
