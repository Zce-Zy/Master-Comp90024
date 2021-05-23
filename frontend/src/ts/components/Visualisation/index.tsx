import React from "react";
import { Col, Row } from "antd";
import { SentimentCard } from "./SentimentCard";

export const Visualisation = () => {
  return (
    <section id="visualisation">
      <Row>
        <Col span={12}>
          <SentimentCard />
        </Col>
      </Row>
    </section>
  );
};
