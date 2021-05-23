import React from "react";
import { Spin } from "antd";

const Spinner = () => {
  return (
    <div className="spinner-container">
      <Spin size="large" />
    </div>
  );
};

export { Spinner };
