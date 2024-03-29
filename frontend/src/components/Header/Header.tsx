// frontend/src/components/Header/Header.tsx

import React from "react";
import { MDBCardHeader } from "mdb-react-ui-kit";

const Header: React.FC = () => {
  return (
    <MDBCardHeader>
      <h1 className="main-header">Evalute Master Theorem</h1>
    </MDBCardHeader>
  );
};

export default Header;
