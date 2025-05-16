<template>
  <VueDatePicker :id="id" :name="id" :vertical="true" :enable-time-picker="false" :auto-apply="true"
    :range="props.range" :required="isRequired" model-type="yyyy-MM-dd" format="dd/MM/yyyy"
    v-bind="$attrs" :model-value="selectedDateRange" :preset-dates="presetDates" class="Date_Picker" :teleport="true"
    :config="{
      allowStopPropagation: false,
      allowPreventDefault: true,
    }" @update:modelValue="handleDate" :week-picker="props.weekPicker">
    <template #preset-date-range-button="{ label, value, presetDate }">
      <span role="button" :tabindex="0" @click="presetDate(value)" @keyup.enter.prevent="presetDate(value)"
        @keyup.space.prevent="presetDate(value)">
        {{ label }}
      </span>
    </template>
    <template #dp-input="">
      <InputField :id="`${id}-input`" density="compact" v-model="inputDates" :name="`${name}-input`"
        prepend-inner-icon="mdi-calendar" :label="placeholder" :readonly="true"
        :isRequired="isRequired" :error-messages="errorMessage" />
    </template>
  </VueDatePicker>
</template>
<script setup>
import VueDatePicker from "@vuepic/vue-datepicker";
import "@vuepic/vue-datepicker/dist/main.css";
import InputField from '@/shared/InputField.vue';
import {
  addMonths,
  addWeeks,
  addYears,
  endOfMonth,
  endOfWeek,
  endOfYear,
  startOfMonth,
  startOfWeek,
  startOfYear,
  subMonths,
  subWeeks,
  subYears,
} from "date-fns";
import moment from "moment";
import { computed } from "vue";
import {
  LAST_MONTH,
  LAST_WEEK,
  LAST_YEAR,
  NEXT_MONTH,
  NEXT_WEEK,
  NEXT_YEAR,
  THIS_MONTH,
  THIS_WEEK,
  THIS_YEAR,
  TODAY,
  YESTERDAY,
} from "./date-range-picker-utils";

// Define props
const props = defineProps({
  id: {
    type: String,
    default: "",
  },
  name: {
    type: String,
    default: "",
  },
  modelValue: {
    type: Object,
    default: () => ({}),
  },
  placeholder: {
    type: String,
    default: "",
  },
  errorMessage: {
    type: Array,
    default: () => [],
  },
  isRequired: {
    type: Boolean,
    default: false,
  },
  clearable: {
    type: Boolean,
    default: true,
  },
  includedPresetDates: {
    type: Array,
    default: () => [
      YESTERDAY,
      TODAY,
      THIS_WEEK,
      THIS_MONTH,
      THIS_YEAR,
      LAST_WEEK,
      LAST_MONTH,
    ],
  },
  range: {
    type: Boolean,
    default: true,
  },
  weekPicker: {
    type: Boolean,
    default: false
  }
});

// Emit events
const emit = defineEmits(["update:modelValue"]);

// Computed properties
const selectedDateRange = computed(() => [
  props.modelValue?.start_date || "",
  props.modelValue?.end_date || "",
]);

const inputDates = computed({
  get() {
    if (props.modelValue?.start_date) {
      const startDate = formatDate(props.modelValue.start_date);
      const endDate = formatDate(props.modelValue.end_date);
      return `${startDate} - ${endDate}`;
    }
    return null;
  },
  set() {
    emit("update:modelValue", {
      start_date: null,
      end_date: null,
    });
  },
});

const presetDates = computed(() => {
  const style = `
    border-bottom: 1px solid #0000002f;
    border-radius: 0px;
    margin-right: 50px;
    padding-inline: 10px;
    padding-block: 10px;
  `;

  const allDates = [
    {
      label: YESTERDAY,
      value: [new Date(new Date().setDate(new Date().getDate() - 1)).toISOString().split("T")[0], new Date(new Date().setDate(new Date().getDate() - 1)).toISOString().split("T")[0]],
      style,
    },
    {
      label: TODAY,
      value: [new Date(), new Date()],
      style,
    },
    {
      label: THIS_WEEK,
      value: [startOfWeek(new Date()), endOfWeek(new Date())],
      style,
    },
    {
      label: LAST_WEEK,
      value: [
        startOfWeek(subWeeks(new Date(), 1)),
        endOfWeek(subWeeks(new Date(), 1)),
      ],
      style,
    },
    {
      label: NEXT_WEEK,
      value: [
        startOfWeek(addWeeks(new Date(), 1)),
        endOfWeek(addWeeks(new Date(), 1)),
      ],
      style,
    },
    {
      label: THIS_MONTH,
      value: [startOfMonth(new Date()), endOfMonth(new Date())],
      style,
    },
    {
      label: LAST_MONTH,
      value: [
        startOfMonth(subMonths(new Date(), 1)),
        endOfMonth(subMonths(new Date(), 1)),
      ],
      style,
    },
    {
      label: NEXT_MONTH,
      value: [
        startOfMonth(addMonths(new Date(), 1)),
        endOfMonth(addMonths(new Date(), 1)),
      ],
      style,
    },
    {
      label: THIS_YEAR,
      value: [startOfYear(new Date()), endOfYear(new Date())],
      style,
    },
    {
      label: LAST_YEAR,
      value: [
        startOfYear(subYears(new Date(), 1)),
        endOfYear(subYears(new Date(), 1)),
      ],
      style,
    },
    {
      label: NEXT_YEAR,
      value: [
        startOfYear(addYears(new Date(), 1)),
        endOfYear(addYears(new Date(), 1)),
      ],
      style,
    },
  ];

  return allDates.filter(
    (presetDate) => props.includedPresetDates.indexOf(presetDate.label) > -1
  );
});

// Methods
const handleDate = (selectedDatesArray) => {
  if (selectedDatesArray) {
    emit("update:modelValue", {
      start_date: props.weekPicker ? selectedDatesArray[0].toLocaleDateString('en-CA') : selectedDatesArray[0],
      end_date: props.weekPicker ? selectedDatesArray[1].toLocaleDateString('en-CA') : selectedDatesArray[1],
    });

  } else {
    emit("update:modelValue", {
      start_date: null,
      end_date: null,
    });
  }
};

const formatDate = (date) => {
  return moment(new Date(date)).format("DD/MM/YYYY");
};

</script>
<style>
.Date_Picker .dp__input_wrap {
  width: 100%;
  box-sizing: inherit !important;
}

.Date_Picker .v-text-field input {
  color: #657484 !important;
}

.Date_Picker .v-field__input {
  padding-top: 0% !important;
  padding-bottom: 0% !important;
}
</style>

