import React from "react";
import { Col, Row } from "antd";
import { SentimentCard } from "./SentimentCard";
import { CrimeRateCard } from "./CrimeRateCard";
import { UnemploymentRateCard } from "./UnemploymentRateCard";

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
        <Col span={12}>
          <UnemploymentRateCard />
        </Col>
      </Row>
    </section>
  );
};
