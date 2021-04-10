import React from "react";
import { Button, Spinner } from "react-bootstrap";

import "./LoaderButton.css";

export default ({
  isLoading,
  text,
  loadingText,
  className = "",
  disabled = false,
  ...props
}) => (
  <Button
    size="lg"
    className={`LoaderButton ${className}`}
    disabled={disabled || isLoading}
    {...props}
  >
    {isLoading && (
      // && <Glyphicon glyph="refresh" className="spinning" />
      <Spinner
        as="span"
        animation="border"
        size="sm"
        role="status"
        aria-hidden="true"
      />
    )}
    {!isLoading ? text : loadingText}
  </Button>
);
