import React, { useState } from "react";
import { Card } from "antd";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faAngleDoubleUp } from "@fortawesome/free-solid-svg-icons";

interface ITitlCardProp {
  title: string;
}

export const TitleCard = ({ title }: ITitlCardProp) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <Card
      title={title}
      bordered={false}
      className={isExpanded ? "expanded" : ""}
      onClick={() => {
        if (!isExpanded) {
          setIsExpanded(!isExpanded);
        }
      }}
    >
      {isExpanded && (
        <>
          <div className="content">
            <div>Content Placeholder</div>
          </div>
          <div className="footer" onClick={() => setIsExpanded(!isExpanded)}>
            <FontAwesomeIcon icon={faAngleDoubleUp} size={"lg"} />
          </div>
        </>
      )}
    </Card>
  );
};
