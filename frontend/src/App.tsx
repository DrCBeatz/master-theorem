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

function App() {
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
          />
          <MDBInput
            label="b (factor by which the problem size is reduced)"
            id="bInput"
            type="number"
            min="2"
            className="my-4"
          />
          <MDBInput
            label="k (exponent in the work done outside the recursive calls)"
            id="kInput"
            type="number"
            min="0"
            className="my-4"
          />

          <MDBBtn href="#" className="btn-block">
            Evaluate
          </MDBBtn>
        </MDBCardBody>
      </MDBCard>

      <MDBCard className="my-5">
        <MDBCardHeader>
          <h2>Evaluation</h2>
        </MDBCardHeader>
        <MDBCardBody>
          <img
            src="plot_example.png"
            className="img-fluid"
            alt="Master Theorem Evaluation"
          />
          <MDBCardText>
            <p>
              <strong>Time Complexity: </strong> Θ(n<sup>k log n</sup>)
            </p>
          </MDBCardText>
          <MDBCardText>
            <p>
              <strong>Evaluation: </strong> Case 2
            </p>
          </MDBCardText>
        </MDBCardBody>
      </MDBCard>
    </>
  );
}

export default App;
