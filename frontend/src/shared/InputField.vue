<script setup>
import { computed } from "vue";

const props = defineProps(["modelValue", "designClass"]);
const emit = defineEmits();

const inputValue = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit("update:modelValue", value);
  },
});

</script>

<template>
  <div>
    <!-- {{  $scopedSlots }} -->
    <VTextField
      autocomplete="new-password"
      v-model="inputValue"
      v-bind="{ ...$attrs }"
      density="compact"
      variant="outlined"
      :class="designClass"
      :label="
        ($attrs && $attrs.required) || $attrs.required === ''
          ? `${$attrs.label} *`
          : `${$attrs.label}`
      "
      :rules="
        ($attrs && $attrs.required) || ($attrs && $attrs.required === '')
          ? $attrs.rules && $attrs.rules.length > 0
            ? [...$attrs.rules]
            : [(val) => !!val || `${$attrs.label} is Required`]
          : $attrs.rules && $attrs.rules.length > 0
          ? [...$attrs.rules]
          : []
      "
    >
      <!-- <template
        v-for="(_, scopedSlotName) in $scopedSlots"
        #[scopedSlotName]="slotData"
      >
        <slot :name="scopedSlotName" v-bind="slotData" />
      </template> -->
      <template v-for="(_, slotName) in $slots" #[slotName]>
        <slot :name="slotName" />
      </template>
    </VTextField>
  </div>
</template>
