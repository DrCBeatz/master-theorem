// frontend/src/App.tsx

import { useState, useEffect, useRef } from "react";
import { SelectData } from "mdb-react-ui-kit/dist/types/pro/forms/SelectV2/types";
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
  MDBAccordion,
  MDBAccordionItem,
  MDBIcon,
  MDBSelect,
} from "mdb-react-ui-kit";

// const CASE_1 = "Case 1: Θ(n<sup>log<sub>b</sub>(a)</sup>)";
// const CASE_2 = "Case 2: Θ(n<sup>k</sup> log n)";
const CASE_3 = "Case 3: Θ(n<sup>k</sup>)";

interface ResultType {
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
  const [tempSelectedAlgorithmDetails, setTempSelectedAlgorithmDetails] =
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
                title: {
                  display: true,
                  text: "Function Value", // Y-axis label
                  color: "#888",
                  font: {
                    size: 12,
                  },
                },
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
                title: {
                  display: true,
                  text: "Input Size (n)", // X-axis label
                  color: "#888",
                  font: {
                    size: 12,
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
            maintainAspectRatio: false,
          },
        });
      }
    }
  }, [showResult, result]);

  // Fetch the list of algorithms on component mount
  useEffect(() => {
    const fetchAlgorithms = async () => {
      try {
        const response = await fetch(
          `${import.meta.env.VITE_API_URL}/algorithms`
        );

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
      setInputsDisabled(false);
      setA("");
      setB("");
      setK("");
      setTempSelectedAlgorithmDetails(null); // Clear temporary algorithm details
    } else {
      const selectedAlgorithm = algorithms.find(
        (alg) => alg.id === algorithmId
      );
      if (selectedAlgorithm) {
        setA(selectedAlgorithm.a.toString());
        setB(selectedAlgorithm.b.toString());
        setK(selectedAlgorithm.k.toString());
        setInputsDisabled(true);
        setTempSelectedAlgorithmDetails(selectedAlgorithm); // Temporarily store the selected algorithm
      }
    }
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const handleSubmitForm = async (event: React.MouseEvent<any>) => {
    event.preventDefault();
    await handleSubmit(event);
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const handleSubmit = async (event: React.MouseEvent<any>) => {
    event.preventDefault(); // Prevent default form submission behavior
    setShowResult(false);

    // Update the displayed algorithm details upon form submission
    setSelectedAlgorithmDetails(tempSelectedAlgorithmDetails);

    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL}/evaluate/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ a, b, k }),
        }
      );

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

  const handleSelectAlgorithm = (data: SelectData | SelectData[]) => {
    // If 'MDBSelect' supports multiple selections, 'data' could be an array
    if (Array.isArray(data)) {
      // This example assumes you're not handling multiple selections for algorithms
      console.log("Multiple selections are not supported.");
    } else {
      // Handle a single selected item
      const algorithmId = parseInt(data.value?.toString() || "-1", 10);

      // Directly call `handleAlgorithmChange` here
      handleAlgorithmChange(algorithmId);
    }
  };

  const selectOptions = [
    { text: "User Input", value: "-1" },
    ...algorithms.map((algorithm) => ({
      text: algorithm.name,
      value: algorithm.id.toString(),
    })),
  ];

  return (
    <>
      <MDBCard alignment="center">
        <MDBCardHeader>
          <h1 className="main-header">Evaluate Master Theorem</h1>
        </MDBCardHeader>
        <MDBCardBody>
          <MDBCardTitle>
            <span className="card-title">
              Enter the values of a, b, and k to evaluate the Master Theorem:
            </span>
          </MDBCardTitle>
          <form onSubmit={handleSubmitForm}>
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
              label="b (factor by which problem size is reduced)"
              id="bInput"
              type="number"
              min="2"
              className="my-4"
              value={b}
              onChange={(e) => setB(e.target.value)}
              disabled={inputsDisabled}
            />
            <MDBInput
              label="k (exponent in the work outside of recursive calls)"
              id="kInput"
              type="number"
              min="0"
              className="my-4"
              value={k}
              onChange={(e) => setK(e.target.value)}
              disabled={inputsDisabled}
            />
            <div className="my-4">
              <MDBSelect
                data={selectOptions}
                label="Choose Algorithm or Enter Values"
                onChange={handleSelectAlgorithm}
              />
            </div>

            <MDBBtn onClick={handleSubmit} className="btn-block">
              Evaluate
            </MDBBtn>
          </form>
        </MDBCardBody>
      </MDBCard>

      {showResult && result && (
        <MDBCard className="my-4">
          <MDBCardHeader>
            <h2>Evaluation</h2>
          </MDBCardHeader>
          <MDBCardBody className="evaluation-card-body">
            <canvas ref={chartRef} id="myChart" className="mb-3"></canvas>

            <MDBCardText>
              <strong>Recurrence Relation: </strong>
              <span
                dangerouslySetInnerHTML={{ __html: result.recurrence_relation }}
              ></span>
            </MDBCardText>
            <MDBCardText>
              <strong>Evaluation: </strong>
              <span dangerouslySetInnerHTML={{ __html: result.case }}></span>
            </MDBCardText>

            {result.case.includes(CASE_3) && ( // Check if the case includes the string for Case 3
              <MDBCardText>
                <strong>Regularity Condition Met:</strong>{" "}
                {result.regularity_condition_met !== undefined && // Check if regularity_condition_met is defined
                  (result.regularity_condition_met ? "Yes" : "No")}
              </MDBCardText>
            )}

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
                  <article>{selectedAlgorithmDetails.description}</article>
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
      <MDBCard alignment="center" className="my-4">
        <MDBCardHeader>
          <h2>About the Master Theorem</h2>
        </MDBCardHeader>

        <MDBAccordion initialActive={1}>
          <MDBAccordionItem
            className="left-align"
            collapseId={1}
            headerTitle="What is the Master Theorem?"
          >
            <article>
              <p>
                The <strong>Master Theorem</strong> offers a straightforward way
                to determine the time complexity of recursive algorithms,
                especially those that follow the divide and conquer approach.
                This theorem simplifies the process of analyzing how efficiently
                an algorithm runs as the size of its input increases. It is
                particularly useful for computer scientists and software
                engineers to predict algorithm performance without the need for
                detailed benchmarks.
              </p>
              <p>
                The following parameters are required to evaluate an algorithm
                using the Master Theorem:
              </p>
              <ul>
                <li>
                  <strong>a</strong> = the number of recursive subproblems.
                </li>
                <li>
                  <strong>b</strong> = the factor by which the problem size is
                  reduced.
                </li>
                <li>
                  <strong>k</strong> = the exponent in the work done outside of
                  the recursive function.
                </li>
              </ul>
            </article>
          </MDBAccordionItem>
          <MDBAccordionItem
            className="left-align"
            collapseId={2}
            headerTitle="Decoding the Master Recurrence"
          >
            <article>
              <p>
                The Master Theorem can only be used to evaluate recursive
                algorithms with the following recurrence relation:
              </p>
              <p className="text-center">
                <strong>T(n) = aT(n/b) + f(n)</strong>
              </p>
              <p>
                This equation is the heart of the Master Theorem. and is called
                the <strong>Master Recurrence</strong>. It captures the essence
                of divide and conquer algorithms:
              </p>
              <ul>
                <li>
                  <strong>T(n)</strong> is the total time complexity we aim to
                  find.
                </li>
                <li>
                  <strong>aT(n/b)</strong> represents the time taken by the
                  recursive subproblems.
                </li>
                <li>
                  <strong>f(n)</strong> is the time taken by the work done
                  outside the recursive calls, such as dividing the problem or
                  combining the results.
                </li>
              </ul>
              <p>
                Evaluating the Master Theorem involves comparing the rate of
                growth of two separate functions:
              </p>
              <ul>
                <p className="text-center">
                  <strong>
                    n<sup>logb(a)</sup> + f(n)
                  </strong>
                </p>

                <li>
                  <strong>
                    n
                    <sup>
                      log<sub>b</sub>(a)
                    </sup>
                  </strong>{" "}
                  is also known as the <strong>watershed function.</strong>
                </li>
                <li>
                  <strong>f(n)</strong> is also known as the{" "}
                  <strong>driving function.</strong>
                </li>
              </ul>
              <p>
                Comparing the growth rate of these 2 functions results in either
                of 3 possible cases.
              </p>
            </article>
          </MDBAccordionItem>
          <MDBAccordionItem
            className="left-align"
            collapseId={3}
            headerTitle="The 3 Cases of the Master Theorem"
          >
            <article>
              <p>
                <strong>Case 1</strong>: n
                <sup>
                  log<sub>b</sub>(a)
                </sup>{" "}
                grows asymptotically and polynomially greater than f(n):
              </p>
              <p className="text-center">
                <strong>
                  T(n) = n
                  <sup>
                    log<sub>b</sub>(a)
                  </sup>
                </strong>
              </p>

              <p>
                <strong>Case 2:</strong> n
                <sup>
                  log<sub>b</sub>(a)
                </sup>{" "}
                and f(n) grow at the same rate:
              </p>
              <p className="text-center">
                <strong>
                  T(n) = n<sup>k</sup> log(n)
                </strong>
              </p>

              <p>
                <strong>Case 3:</strong> f(n) grows assymptotically and
                polynomially greater than n
                <sup>
                  log<sub>b</sub>(a)
                </sup>{" "}
                (and must also fulfill the{" "}
                <strong>
                  regularity condition
                  <sup>*</sup>)
                </strong>{" "}
                :
              </p>
              <p className="text-center">
                <strong>
                  T(n) = f(n<sup>k</sup>)
                </strong>
              </p>
              <ul>
                <li>
                  <strong>Case 1</strong> occurs when the split subproblems
                  dominate the overall time complexity. It implies that as we
                  break the problem down, the sheer number of subproblems is the
                  primary driver of the complexity.
                </li>
                <li>
                  <strong>Case 2</strong> occurs when the work done at each
                  level of recursion is just as significant as the number of
                  subproblems. This balance means the time complexity is a
                  combination of the dividing/conquering work and the depth of
                  the recursion.
                </li>
                <li>
                  <strong>Case 3</strong> highlights scenarios where the work
                  done outside the recursive calls (combining solutions, for
                  instance) is the main factor determining the time complexity.
                  This is typically seen in algorithms where merging or
                  processing results is more intensive than breaking down the
                  problem.
                </li>
              </ul>
              <p>
                <small>
                  <strong>* </strong>
                  The regularity condition ensures that the work done at the
                  recursive levels does not grow too quickly compared to the
                  work done to divide the problem and combine the results. This
                  condition helps maintain the integrity of the complexity
                  analysis provided by the theorem.
                </small>
              </p>
            </article>
          </MDBAccordionItem>
        </MDBAccordion>
      </MDBCard>
    </>
  );
}

export default App;
