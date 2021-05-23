import React from "react";
import { Col, Row } from "antd";
import { SentimentCard } from "./SentimentCard";
import { CrimeRateCard } from "./CrimeRateCard";

export const Visualisation = () => {
  return (
    <section id="visualisation">
      <Row>
        <Col span={12}>
          <SentimentCard />
        </Col>
        <Col span={12}>
          <CrimeRateCard />
        </Col>
      </Row>
    </section>
  );
};
