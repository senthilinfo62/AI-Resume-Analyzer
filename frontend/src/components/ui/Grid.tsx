import { Grid as MuiGrid } from '@mui/material';
import { ReactNode } from 'react';

interface CustomGridProps {
  children: ReactNode;
  container?: boolean;
  item?: boolean;
  xs?: number | boolean;
  sm?: number | boolean;
  md?: number | boolean;
  lg?: number | boolean;
  xl?: number | boolean;
  spacing?: number;
  direction?: 'row' | 'row-reverse' | 'column' | 'column-reverse';
  justifyContent?: 'flex-start' | 'center' | 'flex-end' | 'space-between' | 'space-around' | 'space-evenly';
  alignItems?: 'flex-start' | 'center' | 'flex-end' | 'stretch' | 'baseline';
  sx?: any;
}

export const Grid = (props: CustomGridProps) => {
  return <MuiGrid {...props} />;
};

export default Grid;
