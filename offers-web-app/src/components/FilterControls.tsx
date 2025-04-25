import React from 'react';
import Select from 'react-select';
import type { MultiValue } from 'react-select';

type Option = { value: string; label: string };
type DateRange = { startDate: string | null; endDate: string | null };

type FilterValues = {
  ships: Option[];
  ports: Option[];
  staterooms: Option[];
  offers: Option[];
  nights: Option[];
  destinations: Option[];
  sailDateRange: DateRange;
};

type FilterControlsProps = {
  options: {
    ships: Option[];
    ports: Option[];
    staterooms: Option[];
    offers: Option[];
    nights: Option[];
    destinations: Option[];
  };
  filters: FilterValues;
  onFilterChange: (filters: FilterValues) => void;
  onClear: () => void;
};

export default function FilterControls({
  options,
  filters,
  onFilterChange,
  onClear,
}: FilterControlsProps) {
  const handleSelectChange =
    (key: keyof FilterValues) => (selected: MultiValue<Option>) => {
      onFilterChange({ ...filters, [key]: [...selected] }); // spread to copy into a mutable array
    };

  const handleDateChange =
    (key: keyof DateRange) => (e: React.ChangeEvent<HTMLInputElement>) => {
      onFilterChange({
        ...filters,
        sailDateRange: {
          ...filters.sailDateRange,
          [key]: e.target.value,
        },
      });
    };

  return (
    <div className='p-4 border rounded mb-6 bg-gray-50 space-y-4'>
      <div className='grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4'>
        <div>
          <label className='text-sm font-medium'>Ship Name</label>
          <Select
            isMulti
            options={options.ships}
            value={filters.ships}
            onChange={handleSelectChange('ships')}
          />
        </div>
        <div>
          <label className='text-sm font-medium'>Departure Port</label>
          <Select
            isMulti
            options={options.ports}
            value={filters.ports}
            onChange={handleSelectChange('ports')}
          />
        </div>
        <div>
          <label className='text-sm font-medium'>Stateroom Type</label>
          <Select
            isMulti
            options={options.staterooms}
            value={filters.staterooms}
            onChange={handleSelectChange('staterooms')}
          />
        </div>
        <div>
          <label className='text-sm font-medium'>Offer Type</label>
          <Select
            isMulti
            options={options.offers}
            value={filters.offers}
            onChange={handleSelectChange('offers')}
          />
        </div>
        <div>
          <label className='text-sm font-medium'>Nights</label>
          <Select
            isMulti
            options={options.nights}
            value={filters.nights}
            onChange={handleSelectChange('nights')}
          />
        </div>
        <div>
          <label className='text-sm font-medium'>Destination</label>
          <Select
            isMulti
            options={options.destinations}
            value={filters.destinations}
            onChange={handleSelectChange('destinations')}
          />
        </div>
        <div className='md:col-span-2 lg:col-span-3 flex gap-4 items-end'>
          <div>
            <label className='text-sm font-medium'>Sail Date Start</label>
            <input
              type='date'
              className='border border-gray-300 px-2 py-1 rounded w-full'
              value={filters.sailDateRange.startDate || ''}
              onChange={handleDateChange('startDate')}
            />
          </div>
          <div>
            <label className='text-sm font-medium'>Sail Date End</label>
            <input
              type='date'
              className='border border-gray-300 px-2 py-1 rounded w-full'
              value={filters.sailDateRange.endDate || ''}
              onChange={handleDateChange('endDate')}
            />
          </div>
          <div className='flex gap-2 items-end'>
            <button
              onClick={onClear}
              type='button'
              className='px-4 py-2 border border-gray-300 text-gray-700 rounded hover:bg-gray-100'
            >
              Clear Filters
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
