import React, { useState } from "react";
import './about.scss'
export default function About() {
  const [form, setForm] = useState({ name: "", email: "", message: "" });
  const [status, setStatus] = useState(null);

  function handleChange(e) {
    const { name, value } = e.target;
    setForm((prev) => ({ ...prev, [name]: value }));
  }

  async function handleSubmit(e) {
    e.preventDefault();
    setStatus("sending");

    try {
      await new Promise((res) => setTimeout(res, 500));
      console.log("Contact form submitted:", form);
      setStatus("sent");
      setForm({ name: "", email: "", message: "" });
    } catch (err) {
      setStatus("error");
    }
  }

  return (
    <div className="about-page">
      <section className="about-description">
        <h1>About</h1>
        <p>
          Welcome to my Machine Learning Platform a comprehensive web-based solution
          for data analysis and model development. My platform enables users to upload 
          various data formats (.txt, .csv, Excel) and apply multiple machine learning 
          models including linear regression, logistic regression, decision trees, 
          and advanced ensemble methods like bagging, boosting, and random forests.
        </p>
        <p>
          Users can leverage powerful visualization tools to evaluate model performance 
          through accuracy metrics, and comparative analysis charts. Our
          secure platform requires authentication to access these features, ensuring 
          your data and analysis remain protected.
        </p>
        <p>
          Whether you're a data scientist, researcher, or machine learning enthusiast, 
          our platform provides the tools you need for sophisticated model development 
          and evaluation.
        </p>
      </section>

    </div>
  );
}