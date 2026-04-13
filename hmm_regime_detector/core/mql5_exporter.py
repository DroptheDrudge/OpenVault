import json
import numpy as np
from typing import List


class MQL5Exporter:
    """Export HMM parameters to MQL5-compatible include file."""
    
    def __init__(self, json_path: str):
        with open(json_path, 'r') as f:
            self.params = json.load(f)
    
    def generate_mqh(self, output_path: str, class_name: str = "CHMMRegimeDetector"):
        """Generate an MQL5 .mqh include file."""
        n_regimes = self.params['n_regimes']
        n_features = self.params['n_features']
        
        lines = []
        lines.append(f"// {class_name}.mqh")
        lines.append("// Auto-generated HMM Regime Detector for MQL5")
        lines.append("// Forward algorithm for real-time regime inference")
        lines.append("")
        lines.append("#property strict")
        lines.append("")
        lines.append(f"#define HMM_N_REGIMES   {n_regimes}")
        lines.append(f"#define HMM_N_FEATURES  {n_features}")
        lines.append("")
        lines.append(f"class {class_name}")
        lines.append("{")
        lines.append("private:")
        lines.append(f"   double m_startProb[HMM_N_REGIMES];")
        lines.append(f"   double m_transMat[HMM_N_REGIMES][HMM_N_REGIMES];")
        lines.append(f"   double m_means[HMM_N_REGIMES][HMM_N_FEATURES];")
        lines.append(f"   double m_covars[HMM_N_REGIMES][HMM_N_FEATURES];")
        lines.append("   double m_currentProb[HMM_N_REGIMES];")
        lines.append("")
        lines.append("   double GaussianLogPDF(double observation[], int regime)")
        lines.append("   {")
        lines.append("      double log_prob = 0.0;")
        lines.append("      for(int f = 0; f < HMM_N_FEATURES; f++)")
        lines.append("      {")
        lines.append("         double diff = observation[f] - m_means[regime][f];")
        lines.append("         double var = m_covars[regime][f];")
        lines.append("         if(var < 1e-10) var = 1e-10;")
        lines.append("         log_prob += -0.5 * (diff * diff / var + log(2.0 * M_PI * var));")
        lines.append("      }")
        lines.append("      return log_prob;")
        lines.append("   }")
        lines.append("")
        lines.append("public:")
        lines.append(f"   {class_name}()")
        lines.append("   {")
        lines.append("      InitFromModel();")
        lines.append("      ArrayInitialize(m_currentProb, 0.0);")
        lines.append("      for(int i = 0; i < HMM_N_REGIMES; i++)")
        lines.append("         m_currentProb[i] = m_startProb[i];")
        lines.append("   }")
        lines.append("")
        lines.append("   void InitFromModel(void)")
        lines.append("   {")
        
        # Start probabilities
        for i, val in enumerate(self.params['start_prob']):
            lines.append(f"      m_startProb[{i}] = {val:.10f};")
        lines.append("")
        
        # Transition matrix
        for i, row in enumerate(self.params['transmat']):
            for j, val in enumerate(row):
                lines.append(f"      m_transMat[{i}][{j}] = {val:.10f};")
            lines.append("")
        
        # Means
        for i, row in enumerate(self.params['means']):
            for j, val in enumerate(row):
                lines.append(f"      m_means[{i}][{j}] = {val:.10f};")
            lines.append("")
        
        # Covariances
        for i, row in enumerate(self.params['covars']):
            for j, val in enumerate(row):
                lines.append(f"      m_covars[{i}][{j}] = {val:.10f};")
            lines.append("")
        
        lines.append("   }")
        lines.append("")
        lines.append("   // Update HMM state given new observation")
        lines.append("   // observation[] must have HMM_N_FEATURES elements")
        lines.append("   // Returns most likely regime index")
        lines.append("   int Update(double observation[])")
        lines.append("   {")
        lines.append("      double newProb[HMM_N_REGIMES];")
        lines.append("      ArrayInitialize(newProb, 0.0);")
        lines.append("")
        lines.append("      for(int j = 0; j < HMM_N_REGIMES; j++)")
        lines.append("      {")
        lines.append("         double emission = GaussianLogPDF(observation, j);")
        lines.append("         double sum = 0.0;")
        lines.append("         for(int i = 0; i < HMM_N_REGIMES; i++)")
        lines.append("            sum += m_currentProb[i] * m_transMat[i][j];")
        lines.append("         newProb[j] = sum * MathExp(emission);")
        lines.append("      }")
        lines.append("")
        lines.append("      // Normalize")
        lines.append("      double total = 0.0;")
        lines.append("      for(int j = 0; j < HMM_N_REGIMES; j++)")
        lines.append("         total += newProb[j];")
        lines.append("      if(total > 0.0)")
        lines.append("         for(int j = 0; j < HMM_N_REGIMES; j++)")
        lines.append("            newProb[j] /= total;")
        lines.append("")
        lines.append("      ArrayCopy(m_currentProb, newProb);")
        lines.append("")
        lines.append("      // Return argmax")
        lines.append("      int bestRegime = 0;")
        lines.append("      double bestProb = newProb[0];")
        lines.append("      for(int j = 1; j < HMM_N_REGIMES; j++)")
        lines.append("      {")
        lines.append("         if(newProb[j] > bestProb)")
        lines.append("         {")
        lines.append("            bestProb = newProb[j];")
        lines.append("            bestRegime = j;")
        lines.append("         }")
        lines.append("      }")
        lines.append("      return bestRegime;")
        lines.append("   }")
        lines.append("")
        lines.append("   // Get probability of a specific regime")
        lines.append("   double GetRegimeProb(int regime)")
        lines.append("   {")
        lines.append("      if(regime < 0 || regime >= HMM_N_REGIMES) return 0.0;")
        lines.append("      return m_currentProb[regime];")
        lines.append("   }")
        lines.append("")
        lines.append("   // Reset to start probabilities")
        lines.append("   void Reset()")
        lines.append("   {")
        lines.append("      for(int i = 0; i < HMM_N_REGIMES; i++)")
        lines.append("         m_currentProb[i] = m_startProb[i];")
        lines.append("   }")
        lines.append("};")
        
        with open(output_path, 'w') as f:
            f.write('\n'.join(lines))
