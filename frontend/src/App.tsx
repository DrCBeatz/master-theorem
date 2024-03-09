// frontend/src/App.tsx

import { useState, useEffect, useRef } from "react";
import Chart from "chart.js/auto";
import "./App.css";
import {
  MDBCard,
  MDBCardBody,
  MDBCardTitle,
  MDBCardText,
  MDBCardHeader,
  MDBBtn,
  MDBInput,
  MDBRadio,
  MDBBtnGroup,
  MDBAccordion,
  MDBAccordionItem,
  MDBIcon,
} from "mdb-react-ui-kit";

interface ResultType {
  complexity: string;
  case: string;
  plot_data: {
    n: number[];
    n_log_b_a: number[];
    f_n: number[];
    time_complexity: number[];
  };
}

interface AlgorithmType {
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
  const [a, setA] = useState("");
  const [b, setB] = useState("");
  const [k, setK] = useState("");
  const [result, setResult] = useState<ResultType | null>(null);
  const [showResult, setShowResult] = useState(false);
  const [algorithms, setAlgorithms] = useState<AlgorithmType[]>([]);
  const [inputsDisabled, setInputsDisabled] = useState(false);
  const [selectedAlgorithmDetails, setSelectedAlgorithmDetails] =
    useState<AlgorithmType | null>(null);

  const chartRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    if (
      showResult &&
      result &&
      result.plot_data &&
      chartRef &&
      chartRef.current
    ) {
      const ctx = chartRef.current.getContext("2d");
      if (ctx) {
        new Chart(ctx, {
          type: "line",
          data: {
            labels: result.plot_data.n,
            datasets: [
              {
                label: "n^log_b(a)",
                data: result.plot_data.n_log_b_a,
                borderColor: "blue",
                borderWidth: 1,
                fill: false,
              },
              {
                label: "f(n)",
                data: result.plot_data.f_n,
                borderColor: "red",
                borderWidth: 2,
                fill: false,
                borderDash: [5, 5],
              },
              {
                label: "Time Complexity",
                data: result.plot_data.time_complexity,
                borderColor: "green",
                borderWidth: 2,
                fill: false,
                borderDash: [10, 5],
              },
            ],
          },
          options: {
            scales: {
              y: {
                beginAtZero: true,

                ticks: {},
              },
              x: {
                grid: {
                  display: true,
                },
                ticks: {
                  callback: function (value) {
                    return Number(value).toFixed(0); // Rounds the value to the nearest whole number
                  },
                },
              },
            },
            plugins: {
              legend: {
                display: true,
                position: "top", // Position of the legend
                labels: {
                  boxWidth: 20, // Width of the legend color box
                  padding: 10, // Padding between legend items
                },
              },
              tooltip: {
                enabled: true,
              },
            },
            elements: {
              line: {
                borderWidth: 1, // Set line thickness
              },
              point: {
                radius: 0, // Hide points on the line
              },
            },
            responsive: true,
            maintainAspectRatio: true,
          },
        });
      }
    }
  }, [showResult, result]);

  // Fetch the list of algorithms on component mount
  useEffect(() => {
    const fetchAlgorithms = async () => {
      try {
        const response = await fetch("http://localhost:8000/api/algorithms");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const data = await response.json();
        setAlgorithms(data); // Store fetched algorithms
      } catch (error) {
        console.error("Failed to fetch algorithms:", error);
      }
    };
    fetchAlgorithms();
  }, []);

  const handleAlgorithmChange = (algorithmId: number) => {
    if (algorithmId === -1) {
      // User input selected
      setInputsDisabled(false);
      setA("");
      setB("");
      setK("");
      setSelectedAlgorithmDetails(null);
    } else {
      setInputsDisabled(true); // An algorithm is selected
      const selectedAlgorithm = algorithms.find(
        (alg) => alg.id === algorithmId
      );
      if (selectedAlgorithm) {
        setA(selectedAlgorithm.a.toString());
        setB(selectedAlgorithm.b.toString());
        setK(selectedAlgorithm.k.toString());
        setSelectedAlgorithmDetails(selectedAlgorithm);
      }
    }
  };

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
            disabled={inputsDisabled}
          />
          <MDBInput
            label="b (factor by which the problem size is reduced)"
            id="bInput"
            type="number"
            min="2"
            className="my-4"
            value={b}
            onChange={(e) => setB(e.target.value)}
            disabled={inputsDisabled}
          />
          <MDBInput
            label="k (exponent in the work done outside the recursive calls)"
            id="kInput"
            type="number"
            min="0"
            className="my-4"
            value={k}
            onChange={(e) => setK(e.target.value)}
            disabled={inputsDisabled}
          />

          <MDBBtnGroup className="mt-3 mb-5">
            <MDBRadio
              btn
              btnColor="secondary"
              wrapperTag="span"
              name="algorithmRadio"
              id="algorithmRadioUserInput"
              label="User input"
              defaultChecked
              onChange={() => handleAlgorithmChange(-1)}
            />
            {algorithms.map((algorithm, index) => (
              <MDBRadio
                key={algorithm.id}
                btn
                btnColor="secondary"
                wrapperTag="span"
                name="algorithmRadio"
                id={`algorithmRadio${index + 2}`} // +2 to continue the id sequence
                label={algorithm.name}
                onChange={() => handleAlgorithmChange(algorithm.id)}
              />
            ))}
          </MDBBtnGroup>

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
            <canvas
              ref={chartRef}
              id="myChart"
              width="400"
              height="400"
              className="mb-3"
            ></canvas>
            <MDBCardText>
              <strong>Evaluation: </strong>
              <span dangerouslySetInnerHTML={{ __html: result.case }}></span>
            </MDBCardText>

            <MDBCardText>
              <strong>Time Complexity: </strong>
              <span
                dangerouslySetInnerHTML={{ __html: result.complexity }}
              ></span>
            </MDBCardText>
          </MDBCardBody>

          {selectedAlgorithmDetails && (
            <>
              <h4>{selectedAlgorithmDetails.name} Algorithm</h4>
              <MDBAccordion alwaysOpen initialActive={1}>
                <MDBAccordionItem
                  className="left-align"
                  collapseId={1}
                  headerTitle={
                    <>
                      <MDBIcon fas icon="question-circle" /> &nbsp; Algorithm
                      Description
                    </>
                  }
                >
                  {selectedAlgorithmDetails.description}
                </MDBAccordionItem>
                <MDBAccordionItem
                  collapseId={2}
                  headerTitle={
                    <>
                      <MDBIcon fab icon="python" /> &nbsp; Python Code
                    </>
                  }
                >
                  <pre className="left-align">
                    <code>{selectedAlgorithmDetails.python_code}</code>
                  </pre>
                </MDBAccordionItem>
              </MDBAccordion>
            </>
          )}
        </MDBCard>
      )}
    </>
  );
}

export default App;
